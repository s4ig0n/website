verts=int(input("Enter number of vertices:"))
rows=int(input("Enter number of rows:"))
cols=int(input("Enter number of columns:"))
vertices=list(range(1,verts+1))
edges = []

for r in range(rows):
    for c in range(cols):
        node = r * cols + c +1
        
        if c < cols - 1:
            edges.append((node, node + 1))
        
        if r < rows - 1:
            edges.append((node, node + cols))

print("Vertices:", vertices)
print("Edges:", edges)


