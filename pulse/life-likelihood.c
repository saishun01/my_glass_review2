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
  FILE *fp = NULL;
  FILE *fp2 = NULL;
  char fname[1024] = {0};
  int i = 0;
  int j = 0;
  int sum = 0;
  double mean = 0.;
  double tau = 0.;
  double d_tau = 0.;
  double t[NBINSX] = {0.};

  /* read file name from command line */
  if (argc > 1){
    strncpy(fname, argv[1], 1024);
  }else{
    fprintf(stderr, "no input file!\n");
    exit(1);
  }

  /* read data from file and store data to an array */
  read_data(fname);

  /* calculate mean value, most probable value and so on */

  sum = 0;
  mean = 0.;
  for (i = 0; i < NBINSX; i++){
    t[i] = time_to_us(time[i]);
    if (t[i] > 17) break;
    sum += data[i];
    mean += (double)(data[i])*t[i];
  }



  mean /= (double)sum;
  /* print calculation result */
  printf("total count = %d, mean value = %f\n", 
   sum, mean);
  /* unbinned maximum likelihood method */
  /* likelihood L: */
  /*  L = Pi_i 1/tau e^{-t[i]/tau} (i: loop over events) */
  /*  lnL = Sigma_i -ln(tau) - t[i]/tau; */
  /*  d lnL / d tau = Sigma_i {-1/tau + t[i]/tau^2 } = 0 */
  /*  -> tau = Sigma_i t[i] / Sigma_i 1  */
  /*         = mean                      */
  tau = mean;

  /* calculate the error of tau here */
  /* Delta_tau = 1/sqrt(-{d^2 lnL / (d tau')^2}|_{tau'=tau}) */

  d_tau = tau/sqrt((double)sum);  /* MODIFY THIS */

  /* print calculation result */
  printf("tau = %e, d_tau = %e\n", tau, d_tau);

  /* scan likelihood around the mean and write to file for gnuplot */
  /* estimate positive and negative error separately */
  /* 1 sigma error: the value(time) for lnL_max-1 */
  fp = fopen("life-likelihood.dat", "w");
  /* adjust range and step size in below */
  for (j = -100; j <= 100; j++){
    const double delta = j*0.0005;
    double lnL = 0.;
    for (i = 0; i < NBINSX; i++){
      if(t[i] > 17) break;
      lnL += (double)(data[i])*(-log(tau+delta) - t[i]/(tau+delta));
    }
    fprintf(fp, "%f %f\n", tau+delta, lnL);
  }
  fclose(fp);

  fp2 = fopen("tmp2.scr", "w");
  fprintf(fp2,"set terminal postscript enhanced color lw 3.0\n");
  fprintf(fp2,"set output \"likelihood.ps\" \n");
  fprintf(fp2,"set xlabel \"{/Symbol t} ({/Symbol m}s)\" \n");
  fprintf(fp2,"set ylabel \"LOG LIKELIHOOD (ln(L))\" \n");
  fprintf(fp2,"plot \"life-likelihood.dat\n");
  fclose(fp2);

#ifdef _MSC_VER
  Sleep(1000);
#else
  sleep(1);
#endif

  system("gnuplot tmp2.scr");
  return 0;
}

int read_data(const char * fname) {
  FILE * fp = NULL;
  int i = 0;
  char buff[1024] = {0};
  fp = fopen(fname, "r");
  if (!fp) {
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