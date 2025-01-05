/**
 * @name cwe query
 * @description This is a test query to demonstrate the use of @kind.
 * @kind problem
 * @problem.severity warning
 * @precision high
 * @id java/cwe-query
 */
import java
import semmle.code.java.dataflow.FlowSources
import semmle.code.java.dataflow.TaintTracking
import semmle.code.java.security.ExternalAPIs
import DataFlow::PathGraph

from UntrustedDataToExternalApiConfig config, DataFlow::PathNode source, DataFlow::PathNode sink
where config.hasFlowPath(source, sink)
select sink, source, sink,
  "Call to " + sink.getNode().(ExternalApiDataNode).getMethodDescription() +
    " with untrusted data from $@.", source, source.toString()