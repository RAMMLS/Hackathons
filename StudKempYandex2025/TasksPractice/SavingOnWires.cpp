#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>

using namespace std;

struct Point {
    double x, y, z;
};

double distance(const Point& a, const Point& b) {
    return sqrt((a.x - b.x) * (a.x - b.x) + 
               (a.y - b.y) * (a.y - b.y) + 
               (a.z - b.z) * (a.z - b.z));
}

Point geometricMedian(const vector<Point>& points, double eps = 1e-6, int maxIterations = 100) {
    Point median;
    median.x = 0.0;
    median.y = 0.0;
    median.z = 0.0;
    for (const auto& p : points) {
        median.x += p.x;
        median.y += p.y;
        median.z += p.z;
    }
    median.x /= points.size();
    median.y /= points.size();
    median.z /= points.size();

    for (int iter = 0; iter < maxIterations; ++iter) {
        Point newMedian;
        newMedian.x = 0.0;
        newMedian.y = 0.0;
        newMedian.z = 0.0;
        double totalWeight = 0.0;

        for (const auto& p : points) {
            double dist = distance(median, p);
            if (dist < eps) continue; // избегаем деления на ноль
            double weight = 1.0 / dist;
            newMedian.x += p.x * weight;
            newMedian.y += p.y * weight;
            newMedian.z += p.z * weight;
            totalWeight += weight;
        }

        if (totalWeight == 0.0) break; // все точки совпадают с текущей медианой
        newMedian.x /= totalWeight;
        newMedian.y /= totalWeight;
        newMedian.z /= totalWeight;

        if (distance(median, newMedian) < eps) break;
        median = newMedian;
    }

    return median;
}

int main() {
    int N;
    cin >> N;
    vector<Point> points(N);
    for (int i = 0; i < N; ++i) {
        cin >> points[i].x >> points[i].y >> points[i].z;
    }

    Point server = geometricMedian(points);

    cout << fixed << setprecision(2);
    cout << server.x << " " << server.y << " " << server.z << endl;

    return 0;
}
