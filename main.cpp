#include <iostream>
#include <stdlib.h>

int main() {
  int number = 0;
  std::cout << "Enter a number to determine prime status: ";
  std::cin >> number;
  int divide_by = 2;
  bool is_prime = true;

  while (divide_by != (number / 2)){
      if(number % divide_by == 0){
            is_prime = false;
            break;
      }
      divide_by++;
  }
  if (is_prime) {
    std::cout << number << " is a prime number!";
  } else {
    std::cout << number << " is not prime.";
  }
  return 0;
}
