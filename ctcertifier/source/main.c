#include <string.h>
#include <stdio.h>
#include <3ds.h>

static Handle amHandle;

Result amGetServiceHandle(void)
{
	return srvGetServiceHandle(&amHandle, "am:net");
}

Result amCloseServiceHandle(void)
{
	return svcCloseHandle(amHandle);
}

Result amNetGetDeviceCert(u8 const * buffer) //from https://github.com/joel16/3DSident
{
	Result ret = 0;
	u32 *cmdbuf = getThreadCommandBuffer();

	cmdbuf[0] = IPC_MakeHeader(0x818, 1, 2); // 0x08180042
	cmdbuf[1] = 0x180;
	cmdbuf[2] = (0x180 << 4) | 0xC;
	cmdbuf[3] = (u32)buffer;

	if(R_FAILED(ret = svcSendSyncRequest(amHandle))) 
		return ret;

	return (Result)cmdbuf[1];
}

int main(int argc, char **argv) {

	gfxInitDefault();
	consoleInit(GFX_TOP, NULL);
	Result res;
	u8 ctcert[0x19E]={0};
	
	res = amGetServiceHandle();
	printf("am:net %08X\n",(int)res);
	
	res = amNetGetDeviceCert(ctcert); //thanks joel16 for this
	printf("getcert %08X\n",(int)res);
	memcpy(ctcert+0x180, "ctcert privkey  goes here", 25);
	
	FILE *f=fopen("/ctcert.bin","wb");
	fwrite(ctcert, 1, 0x19E, f);
	fclose(f);
	printf("Done. Press Start to exit\n");


	// Main loop
	while (aptMainLoop()) {

		gspWaitForVBlank();
		hidScanInput();

		// Your code goes here

		u32 kDown = hidKeysDown();
		if (kDown & KEY_START)
			break; // break in order to return to hbmenu

		// Flush and swap framebuffers
		gfxFlushBuffers();
		gfxSwapBuffers();
	}

	gfxExit();
	return 0;
}
