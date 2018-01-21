#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <3ds.h>
#include "fs.h"
#include "types.h"

extern u32 keyy[4];

int main(int argc, char **argv) {

	gfxInitDefault();
	consoleInit(GFX_TOP, NULL);
	Result res;
	
	struct msed_data{
		u32 lfcs_blk;
		s32 msed3offset;
		u32 seedtype;
	} mdata;
	
	//nand to sd copy function from the following. 
	//https://github.com/joel16/3DS-Recovery-Tool Thanks to Joel16 for it.
	res = copy_file( "/private/movable.sed", "/movable.sed");
	
	if(res) printf("Movable.sed dump failed.\n");
	else{
		srand(time(NULL));
		u32 rnd=rand();
		char filename[0x100]={0};
		u32 lfcs=*keyy;
		u32 lfcs_blk=lfcs >> 12;
		u32 msed3=*(keyy+3);
		s32 msed3offset=(lfcs/5)-(msed3&0x7FFFFFFF);
		u32 seedtype=(msed3&0x80000000)>>31;
		printf("Movable.sed dump to sdmc:/ success!\n\n");
		printf("  LFCS  exact  %08lX\n", lfcs);
		printf("* LFCS  block  %08lX\n", lfcs_blk);
		printf("  Msed3 exact  %08lX\n", msed3);
		printf("* Msed3 offset %ld\n", msed3offset);
		printf("* Seedtype     %ld\n", seedtype);
		mdata.lfcs_blk=lfcs_blk;
		mdata.msed3offset=msed3offset;
		mdata.seedtype=seedtype;
		snprintf(filename, 0x100, "/msed_data_%08lX.bin", rnd);
		printf("\n* will be written to\nsdmc:%s\n\n",filename);
		FILE *f=fopen(filename,"wb");
		fwrite(&mdata, 1, sizeof(mdata), f);
		fclose(f);
		printf("Done.\n");
	}
	
	
	
	printf("\nSTART to exit\nB to delete this app\n");

	// Main loop
	while (aptMainLoop()) {

		gspWaitForVBlank();
		hidScanInput();

		u32 kDown = hidKeysDown();
		if (kDown & KEY_START)
			break; // break in order to return to hbmenu
		else if(kDown & KEY_B){
			amInit();
			res = AM_DeleteAppTitle(MEDIATYPE_SD, (u64)0x0004000005333D00);
			if(res) printf("\nSelf-delete failed.\n");
			else    printf("\nSelf-delete success!\n");
			svcSleepThread(500*1000*1000);
			break;
		}
	
		gfxFlushBuffers();
		gfxSwapBuffers();
	}

	gfxExit();
	return 0;
}