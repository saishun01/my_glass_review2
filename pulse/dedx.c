#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define NBINSX (256)  /* <- Modify this if necessary */

int data[NBINSX] = {0};
double voltage[NBINSX] = {0.};

/* read data from file and store them to data[NBINSX] */
int read_data(const char * fname);

double voltage_to_energy(const double x){
  /* energy (in MeV) per x value (MODIFY THIS) */
  return x*99.0 + 5.0;
}
  
/* main routine */
int main(int argc, char ** argv){
  /* input file name */
  char fname[1024] = {0};
  int i = 0;
  /* sum of the number of events */
  int sum = 0;
  /* maximum number of events */
  int max = 0;
  /* most probable value */
  double most_probable = 0.;
  /* <- add lines below for the calculation of the mean value */
  double mean = 0.; 

  /* read file name from command line */
  if (argc > 1){
    strncpy(fname, argv[1], 1024);
  }else{
    fprintf(stderr, "no input file!\n");
    exit(1);
  }

  /* read data from file and store data to an array: data[NBINSX] */
  /* data[NBINSX] contain number of events for corresponding voltage value */
  read_data(fname);

  /* calculate mean value, peak value and so on */
  /* calculate mean value here */
  sum = 0;
  max = 0;
  mean = 0.;
  most_probable = -1.;
  for (i = 0; i < NBINSX; i++){
    /* convert: voltage i -> energy */
    const double energy = voltage_to_energy(voltage[i]);
    /* i-> voltage    data[i] -> number of events for "i" */
    sum += data[i];
    mean += data[i]*energy;

    if (data[i] > max){
      max = data[i];
      most_probable = energy;
    }
  }

  mean = mean / sum;

  /* print calculation result */
  printf("number of events = %d\n", sum);
  printf("most probable energy loss = %e, mean = %e\n", 
   most_probable, mean);

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
        if (2 == sscanf(buff, "%lf %d\n", voltage + i, data + i)) {
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
  fclose(fp);
  return i;
}
