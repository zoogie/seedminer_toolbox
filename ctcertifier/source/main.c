#include "common.h"
#include "descriptions.h"
#include "draw.h"
#include "fs.h"
#include "hid.h"
#include "menu.h"
#include "platform.h"
#include "i2c.h"
#include "decryptor/keys.h"
#include "decryptor/game.h"
#include "decryptor/ak2i.h"
#include "decryptor/nand.h"
#include "decryptor/nandfat.h"
#include "decryptor/titlekey.h"
#include "decryptor/selftest.h"
#include "decryptor/xorpad.h"
#include "decryptor/transfer.h"

#define SUBMENU_START 8

void Reboot()
{
    i2cWriteRegister(I2C_DEV_MCU, 0x20, 1 << 2);
    while(true);
}


void PowerOff()
{
    i2cWriteRegister(I2C_DEV_MCU, 0x20, 1 << 0);
    while (true);
}


u32 InitializeD9(MenuInfo *menu)
{
    u32 errorlevel = 0; // 0 -> none, 1 -> autopause, 2 -> critical
    
    ClearScreenFull(true, true);
    DebugClear();
    #ifndef BUILD_NAME
    DebugColor(COLOR_ACCENT, "-- Decrypt9 --");
    #else
    DebugColor(COLOR_ACCENT, "-- %s --", BUILD_NAME);
    #endif
    
    // a little bit of information about the current menu
    if (sizeof(menu)) {
        u32 n_submenus = 0;
        u32 n_features = 0;
        for (u32 m = 0; menu[m].n_entries; m++) {
            n_submenus = m;
            for (u32 e = 0; e < menu[m].n_entries; e++)
                n_features += (menu[m].entries[e].function) ? 1 : 0;
        }
        Debug("Counting %u submenus and %u features", n_submenus, n_features);
    }
    
    Debug("Initializing, hold L+R to pause");
    Debug("");    
    
    if (InitFS()) {
        char serial[16];
        Debug("Initializing SD card... success");
        FileGetData("d9logo.bin", BOT_SCREEN, 320 * 240 * 3, 0);
        Debug("Build: %s", BUILD_NAME);
        Debug("Work directory: %s", GetWorkDir());
        Debug("Game directory: %s", GetGameDir());
        SetupSector0x96Key0x11(); // Sector0x96 key - no effect on error level
        if (SetupTwlKey0x03() != 0) // TWL KeyX / KeyY
            errorlevel = 2;
        if ((GetUnitPlatform() == PLATFORM_N3DS) && (SetupCtrNandKeyY0x05() != 0))
            errorlevel = 2; // N3DS CTRNAND KeyY
        if (LoadKeyFromFile(0x25, 'X', NULL)) // NCCH 7x KeyX
            errorlevel = (errorlevel < 1) ? 1 : errorlevel;
        if (LoadKeyFromFile(0x18, 'X', NULL)) // NCCH Secure3 KeyX
            errorlevel = (errorlevel < 1) ? 1 : errorlevel;
        if (LoadKeyFromFile(0x1B, 'X', NULL)) // NCCH Secure4 KeyX
            errorlevel = (errorlevel < 1) ? 1 : errorlevel;
        if (SetupAgbCmacKeyY0x24()) // AGBSAVE CMAC KeyY
            errorlevel = (errorlevel < 1) ? 1 : errorlevel;
        GetSerial(serial);
        Debug("Serial number: %s", serial);
        Debug("Finalizing Initialization...");
        RemainingStorageSpace();
    } else {
        Debug("Initializing SD card... failed");
            errorlevel = 2;
    }
    Debug("");
    Debug("Initialization: %s", (errorlevel == 0) ? "success!" : (errorlevel == 1) ? "partially failed" : "failed!");
    
    if (CheckButton(BUTTON_L1|BUTTON_R1) || (errorlevel > 1)) {
        DebugColor(COLOR_ASK, "(A to %s)", (errorlevel > 1) ? "exit" : "continue");
        while (!(InputWait() & BUTTON_A));
    }
    
    return errorlevel;
}

u8 *top_screen, *bottom_screen;

int main(int argc, char** argv)
{
	
	if(argc >= 2) {
        // newer entrypoints
        u8 **fb = (u8 **)(void *)argv[1];
        top_screen = fb[0];
        bottom_screen = fb[2];
    } else {
        // outdated entrypoints
        top_screen = (u8*)(*(u32*)0x23FFFE00);
        bottom_screen = (u8*)(*(u32*)0x23FFFE08);
	}
	
	ClearScreenFull(true, true);

	InitFS();
	if(FileOpen("/seedstarter/ctcert.bin")){
		FileWrite((u8*)0x01FFB826, 0x1E, 0x180);
		Debug("Privkey written to /seedstarter/ctcert.bin");
		DeinitFS();
	}
	else{
		Debug("Failed to open /seedstarter/ctcert.bin");
		//while(1);
	}
	Debug("\nPress any key to power off\n");
	InputWait();
	PowerOff();

    return 0;
}
