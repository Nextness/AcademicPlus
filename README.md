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


# Documentation Standadization

Most of the code in this repository follows a strict documentation format. For each function, there are mandatory fields which need to be included, as well as optional/warning fields. Bellow is a list of the different types of fields and their objectives.

## Documentation Checking
Documentation check is a quality step to check the current fingerprint of the library as a whole, if there is new updates, which are the new updates and changes, if everything is up-to-date, and what needs to be changed or updated. A parse is utilized for that, validating a documentation steps, which are included in different fields inside a function.

## Fields

Mandatory fields are include as part of comments in functions and are necessary to document what the function is utilized, expected behaviour, expected inputs, outputs and the their types, expected return values and the meaning of each return value, etc.

- **Mandatory: \[Tags\]** →
- **Conditional: \[Deprecation Info\]** → This field identifies functions that are no longer supported. It must contain information from when it stoped being supported, the reasoning behind it and the replacement function, if any.
  - **`(Date)`** →
  - **`(Reason)`** →
  - **`(Replacement)`** →
- **Conditional: \[Warnings\]** → This field is a disclaimer for the end user about any specific information they should be aware.
- **Mandatory: \[Description\]** → This field contains the description of the function with its expected behavior. 
- **Mandatory: \[Arguments\]** → This field contains the type of the the argument, followed by its name. It Should also contain a brief description of the argument that is typed as "(Definition)".
  - **`\<type::variable_name\>`** → 
  - **`(Definition)`** →
    - **`Flag_Value`** → 
- **Mandatory: \[Exceptions\]** →
  - **`(Exception)`** →
- **Mandatory: \[Return\]** → This field contains the type of the the return, followed by its name. It Should also contain a brief description of the return that is typed as "(Definition)". It also can cointain the different return types, if the specific function has a specific set of return values and their meaning.
  - **`\<type::variable_name\>`** → 
  - **`(Definition)`** →
    - **`Return_Value`** → 
- **Conditional: \[Video Demonstration\]** →
- **Optional: \[References\]** →


## Template

```python
# FunctionFingerprint: (SHA1) "Hashed_Function_String_Value"
def template_function(argument_1: str, argument_2: dict[str], argument_3: dict[str]) -> dict[str]:
  """
  [Tags]
  | : @IsMaintained bool
  | :   if @IsMaintained == False
  | :   { REMOVE @IsPrivate }
  | : @IsPrivate bool
  | :   if @IsPrivate == False          
  | :   { INCLUDE @DemonstrationCompliant bool }
  | : @HasBug bool
  | :   if @HasBug == True
  | :   { CREATE OR UPDATE [Warning] FIELD AND INCLUDE INFORMATION }
  | : @ToBeDepredated bool
  | :   if ToBeDepredated == True 
  | :   { INCLUDE @DeprecationRelease Release_Number AND @Deprecated bool }
  | : @Deprecated bool
  | :   if @Deprecated == True 
  | :   { REMOVE @ToBeDepredated AND CREATE [Deprecation Info] FIELDS }

  [Deprecation Info]
  | : (Date) YYYY-MM-DD
  | :
  | : (Reason) Explanation of why a function is no longer supported,
  | : with different arguments.
  | :
  | : (Replacement) template_function_new in "Also include the location 
  | : of the new function".

  [Warnings] 
  | : Some warning about this function, such as possible deprecation date,
  | : or that there is a known issue with this function.

  [Description] 
  | : Brief description of the function and what is the expected behaviour.

  [Arguments]
  | : <str::argument_1>
  | : (Definition) Explanation of the argument.
  | :   - FLAG_VALUE_1: Meaning of the flag.
  | :   - FLAG_VALUE_2: Meaning of the flag.
  | :   - FLAG_VALUE_3: Meaning of the flag.
  | :
  | : <dict[str]::argument_2>
  | : (Definition) Explanation of the argument.
  | :
  | : <dict[str]::argument_3>
  | : (Definition) Explanation of the argument.

  [Exceptions]
  | : (ValueError) Description of the error and what may cause it.
  | :
  | : (ValueError) Description of the error and what may cause it.

  [Return]
  | : <dict[str]::dictinary_return>
  | : (Definition) Explanation of the return.
  | :   - RETURN_VALUE_1: Meaning of this return value.
  | :   - RETURN_VALUE_2: Meaning of this return value.

  [Video Demonstration]
  | : (URL) youtube-url
  | :   @VideoVersion => int
  | :   @Duration => HH:MM:SS
  | :   @MinimumQuality => 1080p =< #
  | :   @PublicationDate => YYYY-MM-DD
  | :   @FollowsDemonstrationCriteria => bool
  | :
  | : (HASH) youtube-url SHA1 value.

  [References]
  | : (URL) reference-url
  | :   @Title => TITLE
  | :   @Authors => FirstName LastName, FirstName LastName, ...
  | :   @AccessDate => YYYY-MM-DD
  | :
  | : (HASH) reference-url SHA1 value.
  """
```

## Example