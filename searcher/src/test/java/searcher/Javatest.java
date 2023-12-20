package searcher;

import static org.junit.jupiter.api.Assertions.*;

import java.sql.SQLException;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import searcher.model.Lessee;
import searcher.model.LesseeDAO;
import searcher.model.Payment;
import searcher.model.PaymentDAO;

import javafx.collections.ObservableList;

public class Javatest
{
    //unit test case that will check whether the method returns the
    //anticipated output or not

    @Test
    @DisplayName("test if lessee_id = 1 when lesseename is John Smith")
    
    public void testLesseeNameOnUnit1() throws ClassNotFoundException, SQLException {
        String result = "John Smith"; //lesseeid is 1
        Integer answer = 0;
        try {
            Lessee lessee = LesseeDAO.searchLessee(result);
            answer = lessee.getLesseeId();
        } catch (SQLException e){
            System.out.println("Error occurred while getting lessees information from DB.\n" + e);
            throw e;
        }
        assertEquals(1, answer);
    }

    @Test
    @DisplayName("test if payments are returned when pmt id is 1")

    public void testPaymentID1() throws ClassNotFoundException, SQLException {
        ObservableList<Payment> answers = null;
        try {
            answers = PaymentDAO.searchPayments("a1");
        } catch (SQLException e){
            System.out.println("Error occurred while getting lessees information from DB.\n" + e);
            throw e;
        }
        assertNotNull(answers);
    }
}
