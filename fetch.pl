#!/usr/bin/perl -CDS

use 5.014;

use XML::Feed;
use WWW::Shorten::TinyURL;

# max articles number each feed
use constant THRESHOLD => 5;

open (SUB, "<", "sub");

my @urls;
my @names;
while (my $in = <SUB>) {
    my @tmp = split /\s+/, $in;
    push @urls, $tmp[1];
    push @names, $tmp[0];
}




# goto ./feeds
if (-d "feeds") {
    chdir "feeds";
}
else {
    say "no such dir, make a new one!";
    mkdir "feeds";
    chdir "feeds";
}


for my $name (@names) {
    if (-d $name) {
        chdir $name;
    }
    else {
        say "no such dir, make a new one!";
        mkdir $name;
        chdir $name;
    }

    my $url = shift @urls;

    my $feed = XML::Feed->parse(URI->new($url)) or die XML::Feed->errstr;

    say $feed->title;

    my @data;
    my $count = 0;
    for my $entry ($feed->entries) {
        push @data, [$feed->title, $entry->title, $entry->link];
        $count++;
        last if ($count >= THRESHOLD);
    }

    open (LIST, ">", "list");
    for (@data) {
        say $_->[1];
        say LIST $_->[1];
        my $short =  makeashorterlink($_->[2]);
        say $short;
        say LIST $short;
        say "========";
    }

    chdir "../";
}


