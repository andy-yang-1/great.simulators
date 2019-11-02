requirejs.config({ baseUrl: "../js/Diffenginejs/js" });
requirejs(["edu/sjtu/cs/csdemo/differenceEngine"],
          function(de) { de.DifferenceEngine.main([]); });
