## Mobile Radio Networks project on OpenRAN (M.Sc. Computer Science and Engineering, A.Y. 2023/24) - Politecnico di Milano (PoliMi)

Evaluated positively: 3/3

### License and publishing notes

See [license file](LICENSE)

### Specifications

See [the requirements slideshow](Requirements.pdf)

### Full instruction set

The original base (and updated) repositories are from the [ANTLab](https://github.com/orgs/ANTLab-polimi/repositories) at PoliMi.

1) Install Docker and Docker-compose
2) Clone [this repository](https://github.com/ANTLab-polimi/ric-composer)
   
   `git clone https://github.com/ANTLab-polimi/ric-composer.git`

   `cd ric-composer`
3) Deploy the components (images will be downloaded from Docker Hub)
   
   `docker compose up`
4) In another terminal, open a shell in the gNB container and start the emulator
   
   `docker exec –it gnb bash`

   `./build/gnb_e2server_emu`
5) In another terminal, open a shell in the gNB container and start the E2AP agent
   
   `docker exec –it gnb bash`

   `cd ../ocp-e2sim`

   `./run_e2sim.sh`
6) In another terminal, open a shell in the xApp container and start the xapp
   
   `docker exec –it xapp /bin/sh`

   `python3 myxapp.py`