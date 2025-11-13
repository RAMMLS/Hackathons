#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

//Используем метод скользящего окна (sliding window)

int main() {
  int n, k;
  cin >> n >> k;

  vector<int> coins(n);
  for (int i = 0; i < n; ++i) {
    cin >> coins[i];
  }

  int max_len = 0;
  int left = 0;
  int zeros = 0;

  for (int right = 0; right < n; ++right) {
    if (coins[right] == 0) {
      zeros++;
    }

    while (zeros > k) {
      if (coins[left] == 0) {
        zeros--;
      }
      left++;
    }

    max_len = max(max_len, right - left + 1);
  }

  cout << max_len << endl;

  return 0;
}


