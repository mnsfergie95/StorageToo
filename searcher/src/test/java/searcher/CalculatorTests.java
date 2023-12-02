/*
 * Copyright 2015-2022 the original author or authors.
 *
 * All rights reserved. This program and the accompanying materials are
 * made available under the terms of the Eclipse Public License v2.0 which
 * accompanies this distribution and is available at
 *
 * http://www.eclipse.org/legal/epl-v20.html
 */

package searcher;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class CalculatorTests {

	@Test
	@DisplayName("1 + 1 = 2")
	void addsTwoNumbers() {
		Calculator calculator = new Calculator();
		assertEquals(2, calculator.add(1, 1), "1 + 1 should equal 2");
	}

	@Test
	@DisplayName("2 - 1 = 1")
	void subtractsTwoNumbers() {
		Calculator calculator = new Calculator();
		assertEquals(1, calculator.subtract(2, 1), "2 - 1 should equal 1");
	}

	@Test
	@DisplayName("2 * 3 = 6")
	void multipliesTwoNumbers() {
		Calculator calculator = new Calculator();
		assertEquals(6, calculator.multiply(2, 3), "2 * 3 should equal 6");
	}

	@Test
	@DisplayName("5 / 2 = 2.5")
	void dividesTwoNumbers() {
		Calculator calculator = new Calculator();
		assertEquals(2.5, calculator.divide(5, 2), "5 / 2 should equal 2.5");
	}
}
