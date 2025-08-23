def dijkstra(graph,src):
    v=len(graph)
    dist=[float('inf')for _ in range(v)]
    dist[src]=0
    fin=[False for _ in range(v)]
    for _ in range(v-1):
        u=-1
        for i in range(v):
            if fin[i]==False and(u==-1 or dist[i]<dist[u]):
                u=i
        fin[u]=True
        for j in range(v):
            if graph[u][j]!=0 and fin[j]==False:
                dist[j]=min(dist[j],dist[u]+graph[u][j])
    return dist

edges=[[0,1,4],[0,2,8],[1,4,6],[2,3,2],[3,4,10]]
v=5
graph=[[0 for _ in range(v)]for _ in range(v)]
for u,vv,w in edges:
    graph[u][vv]=w
    graph[vv][u]=w
src = 0
distances=dijkstra(graph,src)
print("shortest path is ",src,":",distances)