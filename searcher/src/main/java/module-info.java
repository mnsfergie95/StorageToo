module searcher {
    
    requires transitive javafx.base;
    requires transitive javafx.controls;
    requires javafx.fxml;
    requires javafx.web;

    requires transitive java.sql.rowset;
   
    opens searcher to javafx.fxml;
    opens searcher.controller to javafx.fxml;
    exports searcher;
}
