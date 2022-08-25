#include <iostream>

#include <stdlib.h>
int item;
struct arraystack { // define an data type ;
    int top;
    int capacity;
    int* array;
};

struct arraystack* createstack (int cap) { // create a stack ;
    struct arraystack* stack;
    stack = (struct arraystack*) malloc (sizeof (struct arraystack));
    stack->top = -1;
    stack->capacity = cap;
    stack->array = (int*) malloc (sizeof (int) * stack->capacity);
    return (stack);
}

int full (struct arraystack* stack) { // checking the stack is full or not.
    if (stack->top == stack->capacity - 1) {
        return (1);
    } else {
        return (0);
    }
}

int empty (struct arraystack* stack) { // checking the stack is empty or not.
    if (stack->top == -1) {
        return (1);
    } else {
        return (0);
    }
}

void push (struct arraystack* stack,
           int item) { // insert elements in the stack ;
    if (!full (stack)) {
        stack->top++;
        stack->array[stack->top] = item;
    }
}

int pop (struct arraystack* stack) { // remove elements from the stack ;
    if (!empty (stack)) {
        item = stack->array[stack->top];
        stack->top--;
        return (item);
    }

    return (-1);
}

int main() {
    int choice;
    struct arraystack* stack;
    stack = createstack (4);

    while (1) {
        printf (" \n 1 . push ");
        printf (" \n 2 . pop ");
        printf (" \n 3 . exit \n ");
        printf (" enter your choice \n ");
        scanf ("%d", &choice);

        switch (choice) {
        case 1:
            printf (" enter a number \n ");
            scanf (" %d ", &item);
            push (stack, item);
            break;

        case 2:
            item = pop (stack);

            if (item == -1) {
                printf (" stack is empty ");
            } else {
                printf (" popped value is %d ", item);
            }

            break;

        case 3:
            exit (0);
        }
    }

    return 0;
}
