#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "frd.h"
#include "utils.h"

int main(int argc, char **argv) 
{
	gfxInitDefault();
	consoleInit(GFX_TOP, NULL);
	Result res;
	u8 lfcs[8];

	res = frdInit();
	printf("frd:u %08X\n",(int)res);
	
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
	
	FILE *f=fopen("friends.txt","w");
	fprintf(f,"Name       : Friend Code    LFCS(BE)         : LFCS(LE)\n"); 
	fprintf(f,"-------------------------------------------------------------\n");
	for (size_t i = 0x0; i < friendCount; i++)
	{
		memcpy(lfcs, &friendKey[i].localFriendCode, 8);
		fprintf(f,"%s : %04llu-%04llu-%04llu %016llX : ", &friendNames[i][0], friendCodes[i]/100000000LL, (friendCodes[i]/10000)%10000, friendCodes[i]%10000, friendKey[i].localFriendCode);
		for(int i=0;i<5;i++){
			fprintf(f,"%02X ",lfcs[i]);
		}
		fprintf(f,"\n");
	}
	fclose(f);
	
	printf("%d friends dumped to friends.txt\n\n",friendCount);
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