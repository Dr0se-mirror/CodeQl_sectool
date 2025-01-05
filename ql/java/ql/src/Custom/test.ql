/**
 * @name 经典 SQL 注入漏洞
 * @description 检测通过字符串拼接构造 SQL 查询，并且用户输入直接用于这些查询的情况。
 * @kind path-problem
 * @problem.severity error
 * @id java/classic-sql-injection
 * @tags security
 *       external/cwe/cwe-089
 */

 import java
 import semmle.code.java.dataflow.DataFlow
 import semmle.code.java.dataflow.TaintTracking
 
 class ClassicSqlInjectionConfig extends TaintTracking::Configuration {
   ClassicSqlInjectionConfig() { this = "ClassicSqlInjectionConfig" }
 
   override predicate isSource(DataFlow::Node source) {
     exists(MethodAccess ma |
       ma.getMethod().hasName("getParameter") and
       source.asExpr() = ma
     )
   }
 
   override predicate isSink(DataFlow::Node sink) {
     exists(MethodAccess ma |
       ma.getMethod().hasName("executeQuery") and
       sink.asExpr() = ma.getArgument(0)
     )
   }

 }
 
 from ClassicSqlInjectionConfig config, DataFlow::PathNode source, DataFlow::PathNode sink
 where config.hasFlowPath(source, sink)
 select sink.getNode(), source, sink,
   "经典 SQL 注入漏洞：用户输入直接用于构造 SQL 查询。"