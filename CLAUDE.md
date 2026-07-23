# cooked-lol conventions

## Classes must always be data-only; logic lives in pure module-level functions

All item and champion stat data is also read only.  
See `DataReadOnlyMeta` for the implementation.  

When touching a module that violates this (method on a class), strip the method into a free function as part of the change.
