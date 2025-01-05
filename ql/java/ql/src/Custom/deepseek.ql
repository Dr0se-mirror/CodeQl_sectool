/**
 * @name deepseek Query
 * @description This is a test query to demonstrate the use of @kind.
 * @kind problem
 * @problem.severity warning
 * @precision high
 * @id java/deepseek-query
 */
import semmle.code.java.dataflow.DataFlow
import semmle.code.java.controlflow.ControlFlow

from MethodCall sourceCall, MethodCall sinkCall, DataFlow.Path path
where
  isInputSource(sourceCall) and
  isDangerousSink(sinkCall) and
  DataFlow.dataFlow(sourceCall, sinkCall, path) and
  not exists(DataFlow.PathStep step |
    step in path.getSteps() and
    step.getCall() instanceof MethodCall mc and
    isValidationStep(mc))
select sourceCall, sinkCall, "Improper input validation detected."