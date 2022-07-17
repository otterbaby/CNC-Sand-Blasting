#include <string.h>


typedef enum signal_codes {low, high} signal;

typedef struct inputs {
  signal mot;
  signal dir;
  signal run;
} input;


//initialization of global tracking variables
input current_input = {0,0,0};
int step_to_go = 0;


/*
 * Exponential function taking only integer arguments.
 */
int tenpower(int base, unsigned int exp){
	int i, result = 1;
	for (i = 0; i < exp; i++)
		result *= base;
	return result;
}


/*
 * Second char is evaluated, "X" and "Y" for respective directions
 */
void dmotor(char *input){
	switch(input[1]){
		case 'Y': current_input.mot = high; break;
		case 'X': current_input.mot = low; break;
		default: break;
	}
}

/*
 * First char is evaluated.
 * "F" and "B" for forward/backward movement.
 */
void ddirect(char *input){
	switch(input[0]){
		case 'B': current_input.dir = high; break;
		case 'F': current_input.dir = low; break;
		default: break;
	}
}


/*
 * Takes variable char array length and sets the number of steps.
 * Input includes the delimiter char!
 */
void dsteps(char *input){
	int i;
	int sum = 0;
	int power = 0;
	//printf("\nInput String is: %s", input);
	for (i = 0; i < strlen(input)-1; i++){
		int num = input[i] - '0';
		power = tenpower(10, strlen(input)-2-i);
		sum += (num * power);
	}
	step_to_go = sum;
	current_input.run = high;
}

/*
 * This is the function pointer to the encryption functions.
 * Its sequence is important for the signal handler.
 */
void (*dfunc[3])(char *input) = {dmotor, ddirect, dsteps};


/*
 * Splits the instructions along the delimiter chars and calls the
 * appropriate encoder function. This can be extended as long as
 * sequence of decoder functions and input string is in order.
 *
 * Delimiters:
 * '%' : start of pay load
 * 't' : end of single instruction
 * '$' : end of pay load
 */

void signal_handler(char *input){
	char out[20];
	volatile int j =0 , i, r = 0;
	//printf("\n%s", input);
	for (i = 0;  i < strlen(input); i++){

		out[r] = input[i];
		r += 1;

		//start of pay load is determined here
		if(input[i] == '%'){
			out[0] = '\0';
			r = 0;
			continue;
		}

		else if (input[i] == 't'){
			out[r] = '\0';
			//printf("\nOutput String is: %s", out);
			//important: sequence hat to be in sync with pointer array
			(*dfunc[j])(out);
			r = 0;
			j++;
			}

	}
}
