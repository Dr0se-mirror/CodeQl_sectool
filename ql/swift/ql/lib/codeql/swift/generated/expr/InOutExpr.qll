// generated by codegen/codegen.py
private import codeql.swift.generated.Synth
private import codeql.swift.generated.Raw
import codeql.swift.elements.expr.Expr

class InOutExprBase extends Synth::TInOutExpr, Expr {
  override string getAPrimaryQlClass() { result = "InOutExpr" }

  Expr getImmediateSubExpr() {
    result =
      Synth::convertExprFromRaw(Synth::convertInOutExprToRaw(this).(Raw::InOutExpr).getSubExpr())
  }

  final Expr getSubExpr() { result = getImmediateSubExpr().resolve() }
}