private import swift
private import DataFlowPrivate
private import TaintTrackingPublic
private import codeql.swift.dataflow.DataFlow
private import codeql.swift.dataflow.Ssa
private import codeql.swift.controlflow.CfgNodes

/**
 * Holds if `node` should be a sanitizer in all global taint flow configurations
 * but not in local taint.
 */
predicate defaultTaintSanitizer(DataFlow::Node node) { none() }

cached
private module Cached {
  /**
   * Holds if the additional step from `nodeFrom` to `nodeTo` should be included
   * in all global taint flow configurations.
   */
  cached
  predicate defaultAdditionalTaintStep(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
    // Flow through one argument of `appendLiteral` and `appendInterpolation` and to the second argument.
    // This is needed for string interpolation generated by the compiler. An interpolated string
    // like `"I am \(n) years old."` is represented as
    // ```
    // $interpolated = ""
    // appendLiteral(&$interpolated, "I am ")
    // appendInterpolation(&$interpolated, n)
    // appendLiteral(&$interpolated, " years old.")
    // ```
    exists(ApplyExpr apply, ExprCfgNode e |
      nodeFrom.asExpr() = [apply.getAnArgument().getExpr(), apply.getQualifier()] and
      apply.getStaticTarget().getName() = ["appendLiteral(_:)", "appendInterpolation(_:)"] and
      e.getExpr() = [apply.getAnArgument().getExpr(), apply.getQualifier()] and
      nodeTo.asDefinition().(Ssa::WriteDefinition).isInoutDef(e)
    )
    or
    // Flow from the computation of the interpolated string literal to the result of the interpolation.
    exists(InterpolatedStringLiteralExpr interpolated |
      nodeTo.asExpr() = interpolated and
      nodeFrom.asExpr() = interpolated.getAppendingExpr()
    )
    or
    // allow flow through string concatenation.
    exists(AddExpr ae |
      ae.getAnOperand() = nodeFrom.asExpr() and
      ae = nodeTo.asExpr() and
      ae.getType().getName() = "String"
    )
    or
    // allow flow through `URL.init`.
    exists(CallExpr call, ClassDecl c, AbstractFunctionDecl f |
      c.getName() = "URL" and
      c.getAMember() = f and
      f.getName() = ["init(string:)", "init(string:relativeTo:)"] and
      call.getFunction().(ApplyExpr).getStaticTarget() = f and
      nodeFrom.asExpr() = call.getAnArgument().getExpr() and
      nodeTo.asExpr() = call
    )
  }

  /**
   * Holds if taint propagates from `nodeFrom` to `nodeTo` in exactly one local
   * (intra-procedural) step.
   */
  cached
  predicate localTaintStepCached(DataFlow::Node nodeFrom, DataFlow::Node nodeTo) {
    defaultAdditionalTaintStep(nodeFrom, nodeTo)
  }
}

import Cached