fun main()
	v:int[ 8192 ];
	i:int;
	n:int;
begin
	print("Entre n: ");
	read(n);
	i := 0 ;
	while i<n do
	begin
		read(v[i]);
		i := i+1
	end
	quicksort( 0 , n-1 , v );
	i := 0  ;
	while i<n-1 do
	begin
		write(v[i]); print(" ");
		if 0 < v[i] - v[ i+1 ] then
		begin
			print("Quicksort falló");
			write(i);
			print("\n");
			return( 0 )
		end
		else
			i:=i+1
	end
	write(v[i]);
	print("Éxito\n")
end