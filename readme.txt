seedminer_toolbox

- msed_data_dumper
This will dump console-unique data that will make future seedminer brute-forces faster by virtue of better
msed3 error correction (if optionally shared). The bottom 12 bits of the LFCS are truncated in the interest 
of maintaining data privacy as much as possible. The files dumped appear like "msed_data_74F224DA.bin", as an example. It is 
12 bytes and consists of: [ LFCS>>12 | msed3 error correct | seedtype(new/old3ds) ] each 4 bytes. This app also dumps
the console's movable.sed itself. This isn't needed for seedminer and certainly shouldn't be shared online.

- hash_clusterer (hash clustering is not implemented currently, so this is useless for now)
Used for the hash_cluster stage3 option in seedminer for greatly improved brute-force speed. 
Put this just inside your Nintendo 3DS folder, run it, and it will add the latest ID0 hash
Do this after each system format. 
Warning: if your system has *received* a system TRANSFER, any subsequent system FORMAT will create 
an entirely different movable.sed compared to the last one. This could throw off any hash_cluster attempt. 
So if you have any suspicion your system was a systransfer recipient, and you haven't formatted since then,
system format once before trying to collect ID0 hashes.

- FriendMiiZero
A way to get the LFCS needed for seedminer if you don't have a userland entrypoint to
run stage1.3dsx. Swap friend codes with someone you trust that can run this homebrew. This will dump
friends.txt which should have your LFCS on it, that hopefully they will give you
without asking for money, or worse (in other words, only do this with people you know). 
This is a demake of FriendMii by Joel16, credits to him.

- Ctcertifier
TADpole needs a valid ctcert from *any* 3ds to create TADs that will pass import checks on a stock 3ds.
To create this file, first run ctcertifier.3dsx on a cfw system (am:net access needed). This will dump 
ctcert.bin to sdmc root. To add the necessary privkey to the ctcert, run ctcertfier.firm and the privkey 
data will be appended to the file in that same location. Of course, both homebrews need to be run on the
same console.

