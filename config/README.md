# Wireless Sofle with rotary encoders and mini joystick

## Updating keymap

1. Make changes and commit to git
2. Push the changes to Github repo to trigger build
3. Download the build artifacts from the "build / Merge Output Artifacts" job from the "Artifact download URL" output
4. Unzip the files and flash the keyboard halves by:
  a. Double-press the flash button to put the keyboard into flash mode
  b. Run `lsblk` to find the keyboard's USB device (usually `/dev/sdX`)
  c. Mount the device with `sudo mount -o gid=users,fmask=113,dmask=002 /dev/sda /mnt/usbstick`
  d. Copy the build file with `sudo cp eyelash_sofle_left\ nice_view-nice_nano_v2-zmk.uf2 /mnt/usbstick`
  e. Unmount with `sudo umount /mnt/usbstick`
  f. Wait until keyboard has restarted, repeat for the other half.
