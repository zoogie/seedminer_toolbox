#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#include "frd.h"
#include "utils.h"

Result dumpFriend(u64 lfcs_share, u64 lfcs_msed, int num){
	Result res;
	char filename[0x100]={0};
	u8 part1[0x1000]={0};
	memcpy(part1, &lfcs_msed, 5);
	snprintf(filename, 0xFF,"/LFCS/%d_%04llu-%04llu-%04llu_part1.sed", num, lfcs_share/100000000LL, (lfcs_share/10000)%10000, lfcs_share%10000);
	FILE *g=fopen(filename,"wb");
	res = fwrite(part1, 1, 0x1000, g);
	fclose(g);
	return res;
}

int main(int argc, char **argv) 
{
	gfxInitDefault();
	consoleInit(GFX_TOP, NULL);
	Result res;
	u8 lfcs[8];

	res = frdInit();
	printf("frd:u %08X\n",(int)res);
	
	mkdir("sdmc:/LFCS", 0777);
	
	size_t friendCount = 0;
	FriendKey friendKey[FRIEND_LIST_SIZE];
	FRD_GetFriendKeyList(friendKey, &friendCount, 0, FRIEND_LIST_SIZE);
	
	MiiStoreData friendMii[FRIEND_LIST_SIZE];
	FRD_GetFriendMii(friendMii, friendKey, friendCount); 
	char friendNames[FRIEND_LIST_SIZE][0x14];
	memset(friendNames, 0, FRIEND_LIST_SIZE*0x14);
	
	//FILE *g=fopen("friends.bin","wb");
	//fwrite(friendMii, 1, sizeof(friendMii[0])*friendCount, g);
	//fclose(g);
	
	u64 friendCodes[FRIEND_LIST_SIZE];
	for (size_t i = 0x0; i < friendCount; i++) 
	{
		FRD_PrincipalIdToFriendCode(friendKey[i].principalId, &friendCodes[i]);
		u16_to_u8(&friendNames[i][0x0], &friendMii[i].name[0], 0x14);
		//memcpy(&friendNames[i][0x0], &friendMii[i].name[0], 0x14);
	}
	
	FILE *f=fopen("/LFCS/friends.txt","w");
	fprintf(f,"\tName       : Friend Code    LFCS(BE)         : LFCS(LE)\n"); 
	fprintf(f,"-----------------------------------------------------------------\n");
	for (size_t i = 0x0; i < friendCount; i++)
	{
		memcpy(lfcs, &friendKey[i].localFriendCode, 8);
		fprintf(f,"%d.\t%s : %04llu-%04llu-%04llu %016llX : ", i, &friendNames[i][0], friendCodes[i]/100000000LL, (friendCodes[i]/10000)%10000, friendCodes[i]%10000, friendKey[i].localFriendCode);
		for(int i=0;i<5;i++){
			fprintf(f,"%02X ",lfcs[i]);
		}
		fprintf(f,"\n");
		res = dumpFriend(friendCodes[i], friendKey[i].localFriendCode&0xFFFFFFFFFFLL, i);
		if(res) printf("Friend %d dumped to LFCS/\n", i);
		else    printf("Friend %d file dump error\n", i);
	}
	fclose(f);
	
	printf("\n%d friends dumped to sdmc:/LFCS\n\n",friendCount);
	printf("Press start to exit\n");
	
	while (aptMainLoop()) 
	{
		hidScanInput();
		u32 kDown = hidKeysDown();
		//u32 kHeld = hidKeysHeld();
		
		if (kDown & KEY_START)
			break;
	}

	gfxExit();
	return 0;
}