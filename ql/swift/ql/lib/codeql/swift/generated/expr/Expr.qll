// generated by codegen/codegen.py
private import codeql.swift.generated.Synth
private import codeql.swift.generated.Raw
import codeql.swift.elements.AstNode
import codeql.swift.elements.type.Type

class ExprBase extends Synth::TExpr, AstNode {
  Type getImmediateType() {
    result = Synth::convertTypeFromRaw(Synth::convertExprToRaw(this).(Raw::Expr).getType())
  }

  final Type getType() { result = getImmediateType().resolve() }

  final predicate hasType() { exists(getType()) }
}