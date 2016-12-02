package Main;

use Getopt::Long;

my $package = 0;

GetOptions(
"package" => \$package
) or croak ("illegal cmdline options");

if ($package)
{
	my $stamp = "commits.txt";

	print "writing revision hash stamp \n";
	open(FILE, ">$stamp") or die "Could not open file: $!";
	print FILE `git config --get remote.origin.url`;
	print FILE `git rev-parse HEAD`;
	close(FILE);

	system("zip", "-r", "builds.zip", "python/bro.py", $stamp, "dist");
}
else
{
	system("python", "setup.py", "bdist_egg");
}
exit();
