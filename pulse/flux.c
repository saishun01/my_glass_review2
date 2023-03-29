#include <stdio.h>
#include <math.h>

int main(void){
  /* modify the following three constants */
  const double x_max = 35.5;
  const double y_max = 35.5;
  const double step = 0.1;
  /* number of events (MODIFY THIS) */
  const int n_events = 14531;
  /* distance between the two scintillator */
  const double d = 8.0;
  /* total time */
  const double time = 1434.4;

  double x1 = 0.;
  double y1 = 0.;
  double x2 = 0.;
  double y2 = 0.;
  /* integral of  dOmega dS' */
  double integ = 0.;
  for (x1 = 0.; x1 < x_max; x1+= step){
    for (y1 = 0.; y1 < y_max; y1+= step){
      for (x2 = 0.; x2 < x_max; x2+= step){
        for (y2 = 0.; y2 < y_max; y2+= step){
          /* write function here to calculate integral */
          integ += pow(d, 4.0)/pow(d*d + (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2), 3.0)*pow(step, 4.0); /* <- Modify this */
        }
      }
    }
  }
  printf ("total time = %f sec \n", time);
  printf ("number of events = %d\n", n_events);
  printf ("integral dOmega dS' = %f sr*cm^2 \n", integ);
  printf ("flux = %f 1/sr/cm^2/s \n", (double)n_events/time/integ);

  return 0;
}
