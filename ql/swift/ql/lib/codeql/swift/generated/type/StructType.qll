// generated by codegen/codegen.py
private import codeql.swift.generated.Synth
private import codeql.swift.generated.Raw
import codeql.swift.elements.type.NominalType

class StructTypeBase extends Synth::TStructType, NominalType {
  override string getAPrimaryQlClass() { result = "StructType" }
}