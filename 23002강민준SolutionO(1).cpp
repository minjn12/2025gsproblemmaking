#include <bits/stdc++.h>
using namespace std;
#define fastio ios_base::sync_with_stdio(0);cin.tie(0);cout.tie(0);
#define ll long long
#define pii pair<int, int>
#define vi vector<int>
#define pb push_back
#define all(v) v.begin(),v.end()
#define st first
#define nd second
#define INF 1073741823

vector<pair<char, pair<int, int>>> v;
int arr[10][10][10];
ll bestScore = -9e18;
vector<int> bestSel;

void dfs(int idx, int picked, int cost, vector<int>& sel)
{
    if(cost > 18 || picked > 7) return;
    if(idx == 25 || picked == 7) {
        if(picked >= 5) {
            bool laneOK[5] = {0, 0, 0, 0, 0};
            for(auto& elem : sel) laneOK[elem/5] = true;
            if(!(laneOK[0] && laneOK[1] && laneOK[2] && laneOK[3] && laneOK[4])) return;
        
            if (cost > 18) return;

            ll sumSk = 0, sumOr = 0;
            for (auto& elem : sel) {
                sumSk += v[elem].second.first;
                sumOr += v[elem].second.second;
            }
            ll score = sumSk * sumOr;
            if (score > bestScore) {
                bestScore = score;
                bestSel = sel;
            }
        }
        return;
    }

    if (25 - idx < 5 - picked) return;

    sel.push_back(idx);
    int price = 5 - (idx % 5);
    dfs(idx+1, picked+1, cost + price, sel);
    sel.pop_back();

    dfs(idx+1, picked, cost, sel);
}

int main()
{
    for(int k=0; k<2; k++) for(int i=0; i<5; i++) for(int j=0; j<5; j++) cin >> arr[k][i][j];
    for(int j=0; j<5; j++) for(int i=0; i<5; i++) v.pb({(char)('A'+i+j*5), {arr[0][i][j],arr[1][i][j]}});
    //for(auto& elem : v) cout << elem.st << " " << elem.nd.st << " " << elem.nd.nd << "\n";
    
    vector<int> sel;
    dfs(0, 0, 0, sel);
    cout << bestScore << "\n";
    sort(bestSel.begin(), bestSel.end(),
         [&](int a, int b){ return v[a].first < v[b].first; });
    for (auto&elem : bestSel) 
      cout << v[elem].first << " ";
    cout << "\n";
}