#include <list>
#include <iostream>
#include <string>
#include <vector>

using namespace std;
  
int main(int argc, const char * argv[]) {
  int lower_config = 0;
  int upper_config = 0;
  int times_to_sort = 0;

  //Get configs for primes
  bool get_configs = false;

  while (get_configs != true){
    cout << "Lower config: ";
    cin >> lower_config;
    cout << "Upper config: ";
    cin >> upper_config;
    times_to_sort = upper_config - lower_config;
    get_configs = true;
  }

  //create vector
  vector<int> candidates;

  //check for obvious non primes
  for (int value = lower_config; value <= upper_config; value++){
    int last_digit = value % 10;
    int last_test = last_digit % 2;
    if (last_test == 0 || last_digit == 5){
    } else {
      candidates.push_back(value);
    }
  }

  cout << "Made list of " << candidates.size() << " candidates long.";

  vector<int> isprime;
  for (int x = 0; x < candidates.size(); x++) {
    //terribly inefficient but it's getting there
    //improvements to come (I hope)
    int value = candidates[x];
    bool testing = true;
    bool prime = true;
    int y = 2;
    while (testing) {
      if (value % y == 0){
        testing = false;
        prime = false;
      } else {
        continue;
      }

      if (prime == true) {
        isprime.push_back(value);
      }
    }
  }

  cout << "Found " << isprime.size() << " prime numbers in given range: ";
  for (int x = 0; x < isprime.size(); x++) {
    int primeNumber = isprime[x];
    cout << primeNumber;
  }

  return 0;

}

