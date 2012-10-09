fun quicksort(l:int, r:int, a:int[8192])
i:int;
j:int;
x:int;
w:int;
tmp:int;
done:int;
begin
i := l;
j := r;
x := a[(l+r)/2];
done := 0;
while done == 0 do
begin
while a[i] < x do
i := i + 1;
while x < a[j] do
j := j - 1;
if i <= j then
begin
tmp := a[i];
a[i] := a[j];
a[j] := tmp;
i:=i+1;