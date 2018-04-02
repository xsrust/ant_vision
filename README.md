# ant_vision
Housing for Honors Project Code

## To run the code, simply run the following:
- `import ant_vision`
- `ant_vision.start()`
- ctrl-c will terminate the program

### some options are configureable through options.json
- number of threaded workers (2 by default)
- threshold between background and foreground (will need tuned per-installation)
- size of open/close kernels(will need tuned per-installation)
- webcam opencv id (0 by default)

## Dependancies are as follows (experimantal setup):
python >= 3.4 (3.6.4)
opencv >= 3.0.0 (3.4.0)
numpy
matplotlib
