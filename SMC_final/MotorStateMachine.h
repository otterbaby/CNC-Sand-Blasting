
typedef enum state_codes {def, mxfw, mxbw, myfw, mybw} st_code;

struct transitions {
	signal mot;
	signal dir;
	signal run;
	st_code state_code;
};


//initialization of global tracking variables
st_code current_state = def;


/*
 * Definitions for the output ports. Pins 4 and 7 are
 * the enable and direction instructions for the motor
 * in X direction and pins 5 and 3 for the motor in Y
 * direction respectively.
 */
#define RESETD 	PORTD = PORTD | B00100000
#define RESETC  PORTC = PORTC | B00010000
#define MX_EN   PORTD = PORTD & B11011111
#define MY_EN   PORTC = PORTC & B11101111
#define FWD 	  PORTD = PORTD | B00001000
#define BWD 	  PORTD = PORTD & B11110111


/*
 * State machine can be extended by appending a function
 * and extending the function pointer and state_code enum.
*/
void default_state(void){
	RESETD;
  RESETC;
}

void mxfw_state(void){
  MX_EN;
	FWD;
}

void mxbw_state(void){
  MX_EN;
	BWD;
}

void myfw_state(void){
  MY_EN;
	FWD;
}

void mybw_state(void){
	MY_EN;
	BWD;
}


/*
 * this is the function pointer to every function above,
 * name need to be in sync for the enum state_codes
*/
void (*mstate[5])(void) = {default_state, mxfw_state, mxbw_state,
							 myfw_state, mybw_state};


//number of possible combinations of binary input bits n^2
#define TRANSITIONS 8

/*
 * Lookup table of all state transitions; has to be in sync
 * with function pointer/enum.
 */
const struct transitions state_transitions[][TRANSITIONS] = {
		{{low, low, low, def},
		{low, low, high,  mxfw},
		{low, high, low, def},
		{low, high, high, mxbw},
		{high, low, low, def},
		{high, low, high, myfw},
		{high, high, low, def},
		{high, high, high, mybw}},

		{{low, low, low, def},
		{low, low, high,  mxfw},
		{low, high, low, def},
		{low, high, high, mxfw},
		{high, low, low, def},
		{high, low, high, mxfw},
		{high, high, low, def},
		{high, high, high, mxfw}},

		{{low, low, low, def},
		{low, low, high,  mxbw},
		{low, high, low, def},
		{low, high, high, mxbw},
		{high, low, low, def},
		{high, low, high, mxbw},
		{high, high, low, def},
		{high, high, high, mxbw}},

		{{low, low, low, def},
		{low, low, high,  myfw},
		{low, high, low, def},
		{low, high, high, myfw},
		{high, low, low, def},
		{high, low, high, myfw},
		{high, high, low, def},
		{high, high, high, myfw}},

		{{low, low, low, def},
		{low, low, high,  mybw},
		{low, high, low, def},
		{low, high, high, mybw},
		{high, low, low, def},
		{high, low, high, mybw},
		{high, high, low, def},
		{high, high, high, mybw}},
};

/*
 * Invokes current state as first array dimension and
 * checks for commands. Returns next state.
 */
st_code lookup(st_code cur, input inp){
	for (int i = 0; i < TRANSITIONS; i++){
		if(state_transitions[cur][i].mot == inp.mot
				&& state_transitions[cur][i].dir == inp.dir
				&& state_transitions[cur][i].run == inp.run)

			return state_transitions[cur][i].state_code;
	}

	return cur;
}


/*
 * Calls the next state by invoking lookup transition
 * with current state/command.
 */
void state_handler(void){
	st_code nextState = lookup(current_state, current_input);
	(*mstate[nextState])();
}
