package searcher;

import java.sql.ResultSet;
import java.sql.SQLException;
 
import searcher.util.DBUtil;

public class FixPhone {
    public static void main(String[] args) throws SQLException, ClassNotFoundException {
        try {
            String phoneFormatted = "";
            DBUtil.dbConnect();
            String sqlStmt = "SELECT * FROM lessee WHERE 1";
            ResultSet rsLessee = DBUtil.dbExecuteQuery(sqlStmt);
            int rowCount = rsLessee.getFetchSize();
            System.out.println("rows returned is " + rowCount);
            while (rsLessee.next()) {
                String phoneStr = rsLessee.getString("phone");
                Integer lesseeID = rsLessee.getInt("lessee_id");
                if ((phoneStr.length() == 7) || (phoneStr.length() == 10)) {
                    phoneFormatted = phoneStr.replaceFirst("(\\d{3})(\\d{3})(\\d+)", "($1) $2-$3");
                    String sqlUpdate = "UPDATE lessee SET phone = '" + phoneFormatted + "' WHERE lessee_id = " + lesseeID;
                    System.out.println("phonestr is "+phoneStr);
                    System.out.println("phoneFormatted is "+phoneFormatted);
                    System.out.println("sqlupdate is "+sqlUpdate);
                    DBUtil.dbExecuteUpdate(sqlUpdate);
                }
            }
        } catch (SQLException e) {
            System.out.println("error is "+ e);
            throw e;
        }

    }
}
