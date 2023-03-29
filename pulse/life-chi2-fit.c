#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

#ifdef _MSC_VER
#include <Windows.h>
#else
#include <unistd.h>
#endif

#define NBINSX (16384)  /* <- Modify this if necessary */
#define NREBIN (256) /* <- Modify this if necessary */

int data[NBINSX] = {0};
double time[NBINSX] = {0.};

/* read data from file and store them to data[NBINSX] */
int read_data(const char * fname);

double time_to_us(const double t) {
  /* time (in micro sec) per x value */
  return (t*1.e+06);
}

/* main routine */
int main(int argc, char ** argv){
  char fname[1024] = {0};
  FILE *fp = NULL;
  FILE *fp2 = NULL;
  int i = 0;
  int j = 0;
  int k = 0;
  int l = 0;

  /* n: histogram with reduced bins: data[NBINSX]->n[NREBIN] */
  double n[NREBIN] = {0.};
  /* y: natural logarithm of n[NREBIN]: y[i]=log(n[i]) */
  double y[NREBIN] = {0.};
  /* ey: error of y */
  double ey[NREBIN] = {0.};
  /* time */
  double t[NREBIN] = {0.};

  double E[2][2] = {{0.,0.}};
  /* error matrix */
  double sigma[2][2] = {{0.,0.}};
  /* solution of the fit: f(t) = alpha[0] + alpha[1] t */
  double alpha[2] = {0.};
  double beta[2] = {0.};
  double det = 0.;
  double tmin_bin = 0.;
  double tmax_bin = 0.;
  double dt_bin = 0.;
  int nbins_merge = 0;
  int merge = 0;
  double tau = 0.;
  double dtau = 0.;
  double chi2 = 0.;
  int count_fit = 0;
  int dof = 0;

  /* read file name from command line */
  if (argc > 1){
    strncpy(fname, argv[1], 1024);
  }else{
    fprintf(stderr, "no input file!\n");
    exit(1);
  }

  /* read data from file and store data to an array */
  read_data(fname);

  merge = (NBINSX+NREBIN-1) / NREBIN;
  if (NBINSX >= NREBIN) {
    nbins_merge = NREBIN;
  }
  else {
    nbins_merge = NBINSX;
  }
  /* merge merge=(NBINSX+NREBIN-1)/NREBIN bins */
  /* to one bin to increase statistics */
  /* number of events for merged bins: n[j] */
  /* \Sigma_{i=j*merge}^{(j+1)*merge} data[i] = n[j] */
  for (j = 0; j < NREBIN; j++) n[j] = 0.;
  for (i = 0; i < NBINSX; i++) n[i/merge] += (double)(data[i]);
  /* central value of the bin */
  /* time for merged bins: t[j] */
  if (nbins_merge > 1) {
    dt_bin = time[1] - time[0];
    for (j = 0; j < nbins_merge; j++) {
      tmin_bin = time_to_us(time[merge*j] - 0.5*dt_bin);
      tmax_bin = time_to_us(time[merge*(j + 1) - 1] + 0.5*dt_bin);
      t[j] = 0.5*(tmin_bin + tmax_bin);
    }
  }
  else {
    t[0] = time_to_us(time[0]);
  }

  /* log(n[j]) -> y[j] +- ey[j] */
  fp=fopen("life-merged-bins.dat", "w");
  for (j = 0; j < nbins_merge; j++){
    if (n[j]>0){ /* number of events > 0 */
      /* calculate logarithm of the number of events */
      y[j] = log(n[j]);
      /* calculate its error */
      /* ey[j] = ... */
    ey[j] = 1./sqrt(n[j]) ;  /* <- Modify this */
      /* write values to the file (life-merged-bins.txt) for gnuplot */
      fprintf(fp,"%f %f %f\n", t[j], y[j], ey[j]);
    }else{ /* number of events = 0 */
      y[j] = -1.;
      ey[j] = -1.;
    }
  }
  fclose(fp);

  /* linear minimum chi square fit                                   */
  /* f(t) = \Sigma_k alpha[k] t^k (k=0,1 in this fit)                */
  /* ( f(t) = alpha[0] + alpha[1] t )                                */
  /* d chi^2/d a[k] = \Sigma_i (f(t[j])-y[j])/(ey[j])^2 * t[j]^k = 0 */
  /* expression in matrix: beta = E alpha                            */
  /* where                                                           */
  /* alpha[k]-> solution of the fit                                  */
  /* beta[k] = \Sigma_j t[j]^k * y[j] / ey[j]^2                      */
  /* E[k][l] = \Sigma_j t[j]^(k+l) / ey[j]^2                         */

  /* initialize beta[k] and E[m][n] */
  for (k = 0; k < 2; k++){
    beta[k] = 0.;
    for (l = 0; l < 2; l++) E[k][l] = 0.;
  }

  /* calculate beta[k] and E[m][n] */
  for (j = 0; j < nbins_merge; j++){
    if (ey[j] < 0) continue; /* ignore empty bin */
    if (t[j] > 17. && t[j] < 20.) continue; /*ignore peak at 18 us*/
    if (n[j] < 30.) break; /* ignore mu <~ 10 */
    const double w=1./ey[j]/ey[j];
    beta[0] +=      y[j]*w;
    beta[1] += t[j]*y[j]*w;
    E[0][0] +=           w;
    E[1][0] +=      t[j]*w;
    E[0][1] +=      t[j]*w;
    E[1][1] += t[j]*t[j]*w;
  }

  /* invert covariant matrix E */
  /* alpha = E^{-1} beta = sigma beta */
  /* error matrix: sigma = E^{-1} */
  det = E[0][0]*E[1][1]-E[0][1]*E[1][0];
  sigma[0][0] =  1./det*E[1][1];
  sigma[0][1] = -1./det*E[0][1];
  sigma[1][0] = -1./det*E[1][0];
  sigma[1][1] =  1./det*E[0][0];

  /* calculate alpha: alpha = sigma beta */
  /* error of alpha: diagonal part of the error matrix, sigma */
  alpha[0] = sigma[0][0]*beta[0]+sigma[1][0]*beta[1];
  alpha[1] = sigma[1][0]*beta[0]+sigma[1][1]*beta[1];
  printf("f(t) = alpha[0] + alpha[1] t\n");
  printf("alpha[0] = %f +- %f\n", alpha[0], sqrt(sigma[0][0]));
  printf("alpha[1] = %f +- %f\n", alpha[1], sqrt(sigma[1][1]));
  /* print tau and its error here */
  tau = -1./alpha[1];
  dtau = sqrt(sigma[1][1])/alpha[1]/alpha[1];
  printf("tau = %f +- %f\n", tau, dtau);

  /* calculate chi square here */
  for (j = 0; j < nbins_merge; j++){
    if (ey[j] < 0) continue; /* ignore empty bin */
    if (t[j] > 17. && t[j] < 20.) continue; /*ignore peak at 18 us*/
    if (n[j] < 30.) break; /* ignore mu <~ 10 */
    printf("t = %f, y = %f, dy = %f, err = %f, n = %f, chi2 += %f\n", t[j], y[j], ey[j], y[j] - alpha[0] - alpha[1]*t[j], n[j], pow((y[j] - alpha[0] - alpha[1]*t[j])/ey[j], 2.)); /*テスト用*/
    chi2 += pow((y[j] - alpha[0] - alpha[1]*t[j])/ey[j], 2.);
    count_fit += 1;
  }  
  dof = count_fit - 2;
  printf("chi2 = %f\n", chi2);
  printf("dof = %d\n", dof);
  printf("chi2/n = %f\n", chi2/dof);

  /* for gnuplot */
  fp2 = fopen("tmp.scr", "w");
  fprintf(fp2,"set terminal postscript enhanced color lw 3.0\n");
  fprintf(fp2,"set output \"life.ps\" \n");
  fprintf(fp2,"set xlabel \"TIME ({/Symbol m}s)\" \n");
  fprintf(fp2,"set ylabel \"ln(COUNTS/bin)\" \n");
  fprintf(fp2,"plot \"life-merged-bins.dat\" with yerrorbar, %f*x+%f\n", 
    alpha[1], alpha[0]);
  fclose(fp2);

#ifdef _MSC_VER
  Sleep(1000);
#else
  sleep(1);
#endif

  system("gnuplot tmp.scr");
  return 0;
}

int read_data(const char * fname){
  FILE * fp = NULL;
  int i = 0;
  char buff[1024] = {0};
  fp=fopen(fname, "r");
  if (!fp){
    fprintf(stderr, "wrong input file: %s!\n", fname);
    exit(1);
  }
  i = 0;
  while (1) {
    if (i < NBINSX) {
      if (fgets(buff, sizeof(buff), fp) != NULL) {
        if (2 == sscanf(buff, "%lf %d\n", time + i, data + i)) {
          ++i;
        }
      }
      else {
        fprintf(stderr, 
          "Error. NBINSX (%d) is larger than the input data. Aborted.", NBINSX);
        exit(1);
      }
    }
    else {
      if (fgets(buff, sizeof(buff), fp) == NULL) {
        break;
      }
      else {
        fprintf(stderr, 
          "Error. NBINSX (%d) is smaller than the input data. Aborted.", NBINSX);
        exit(1);
      }
    }
  }
  return i;
}