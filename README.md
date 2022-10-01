# AcademicPlus

This library has the objective o evaluating `.bib` and `.tex` file inside a folder and parse into a dictonary to be used in further research analysis.

To run the interface, just use the command `./run.bat --type python` for windows. The Linux version will be included later.

# TODO

- [x] Create a dataclass for all the different formats utilized in this library to make it easier to port if necessary;
- [ ] Refactor the code to support dataclasses and improve performance;
  - [ ] Refactor functions to utilize dataclasses already created;
  - [ ] Refactor parsers to increase performance;
- [ ] Transfer all the functions into Cython;
- [ ] 100% Library unit test coverage;
- [ ] Include Linux shell script to run the interface and unit test.