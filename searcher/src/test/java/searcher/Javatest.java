package searcher;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.sql.SQLException;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import searcher.model.Lessee;
import searcher.model.LesseeDAO;

public class Javatest
{
    //unit test case that will check whether the method returns the
    //anticipated output or not

    @Test
    @DisplayName("test if lesseename is John Smith when lessee_id = 1")
    
    public void testLesseeNameOnUnit1() throws ClassNotFoundException, SQLException {
        String result = "John Smith"; //lesseeid is 1
        String answer = null;
        try {
            Lessee lessee = LesseeDAO.searchLessee(1);
            answer = lessee.getLesseeName();
        } catch (SQLException e){
            System.out.println("Error occurred while getting lessees information from DB.\n" + e);
            throw e;
        }
        assertEquals(result, answer);
    }

    @Test
    @DisplayName("test if payment is returned when pmt id is 1");

    public void testPaymentID1() throws ClassNotFoundException, SQLException {
        String answer = null;
        try {
            ObservableList<Payment> answer = PaymentDAO.searchPayments("a1");
        } catch (SQLException e){
            System.out.println("Error occurred while getting lessees information from DB.\n" + e);
            throw e;
        }
        assertNotNull(answer);
}
