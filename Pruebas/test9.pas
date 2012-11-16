fun fib(n:int)
begin
	if(n<2) return 1;
	return fib(n-1) + fib(n-2)
end

fun main()
n:int;
begin
	print("n=");
	read(n);
	write(fib(n))
end