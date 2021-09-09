#include <iostream>
#include <stdlib.h>

int main() {
  int number = 0;
  bool check_style_stats = true;
  while (check_style_stats){
    std::cout << "Enter a number to determine prime status: ";
    std::cin >> number;
    if (number % 2 == 0 || number % 5 == 0) {
      std::cout << "This number is not prime.";
      return 0;
    } else {
      check_style_stats = false;
    }
  }

  int divide_by = 2;
  bool is_prime = true;

  while (divide_by != (number / 2)){
      if (number % divide_by == 0){
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
