/* Standard Stuff */
#include <string.h>
#include <stdio.h>

/* Required Hubo Headers */
#include <hubo.h>

/* For Ach IPC */
#include <errno.h>
#include <fcntl.h>
#include <assert.h>
#include <unistd.h>
#include <pthread.h>
#include <ctype.h>
#include <stdbool.h>
#include <math.h>
#include <inttypes.h>
#include "ach.h"
#include <sys/time.h>  
#include <stdlib.h>


/* Ach Channel IDs */
ach_channel_t chan_hubo_ref;      // Feed-Forward (Reference)
ach_channel_t chan_hubo_state;    // Feed-Back (State)

int main(int argc, char **argv) {

    /* Open Ach Channel */
    int r = ach_open(&chan_hubo_ref, HUBO_CHAN_REF_NAME , NULL);
    assert( ACH_OK == r );

    r = ach_open(&chan_hubo_state, HUBO_CHAN_STATE_NAME , NULL);
    assert( ACH_OK == r );



    /* Create initial structures to read and write from */
    struct hubo_ref H_ref;
    struct hubo_state H_state;
    memset( &H_ref,   0, sizeof(H_ref));
    memset( &H_state, 0, sizeof(H_state));

    /* for size check */
    size_t fs;

    /* Get the current feed-forward (state) */
    r = ach_get( &chan_hubo_state, &H_state, sizeof(H_state), &fs, NULL, ACH_O_LAST );
    if(ACH_OK != r) {
        assert( sizeof(H_state) == fs );
    }

    // Get in the right position for waiving your hand
	H_ref.ref[LSR] = 0.5;
	H_ref.ref[LSP] = -0.3;
	H_ref.ref[LSY] = 1;
	H_ref.ref[LEB] = -2;
	
	/* Write to the feed-forward channel */
    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
    
    
    struct timeval tim;  
    gettimeofday(&tim, NULL);  
    double tic, toc;
    
    tic = tim.tv_sec + (tim.tv_usec/1000000.0);     
    while(1)	// Check how long it will take to go to the waving position
    {
		usleep(.005e6);
		r = ach_get( &chan_hubo_state, &H_state, sizeof(H_state), &fs, NULL, ACH_O_LAST );
		if(ACH_OK != r) { 
			assert( sizeof(H_state) == fs );
		}
		printf("Joint LSR = %f\r\n", H_state.joint[LSR].pos);
		if (fabs(H_state.joint[LSR].pos - H_ref.ref[LSR]) < 0.01)
		{
			gettimeofday(&tim, NULL);  
			toc = tim.tv_sec+(tim.tv_usec/1000000.0);  
			printf("%.6lf seconds elapsed\n", toc - tic);
			break;
		}
	}
    
    double period = 1e6;
	int nWaves = 30;
	while(1)	// Start waiving and time yourself
	{
		gettimeofday(&tim, NULL);  
		tic = tim.tv_sec+(tim.tv_usec/1000000.0); 
		
		H_ref.ref[LEB] = -1;
		/* Write to the feed-forward channel */
		ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
		
		usleep(period/2.0);
		
		H_ref.ref[LEB] = -2.5;
		/* Write to the feed-forward channel */
		ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));
		
		usleep(period/2.0);
		
		nWaves = nWaves - 1;
		if (nWaves < 0)
		{
			printf("waving done!");
			break;
		}
		
		gettimeofday(&tim, NULL);  
		toc = tim.tv_sec+(tim.tv_usec/1000000.0);  
		printf("Period is: %.6lf \n", toc - tic);
		printf("%d waves left!\n", nWaves);
	} 
    
    // Go back to zeros
	H_ref.ref[LSR] = 0;
	H_ref.ref[LSP] = 0;
	H_ref.ref[LSY] = 0;
	H_ref.ref[LEB] = 0;
	
	/* Write to the feed-forward channel */
    ach_put( &chan_hubo_ref, &H_ref, sizeof(H_ref));

}

