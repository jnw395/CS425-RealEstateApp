
-- Neighborhood
INSERT INTO neighborhood VALUES
('Downtown', 35.50, 'Central High', 'Liberty Park'),
('Uptown', 20.00, 'North Ridge', 'Greenbelt Park'),
('Midtown', 45.75, 'Westview School', 'Midtown Park'),
('Suburbia', 15.30, 'Sunnydale School', 'Oak Park'),
('Harborview', 28.60, 'Seaside Academy', 'Harbor Park');

-- User
INSERT INTO "user" VALUES
('alice@example.com', 'Alice', 'Wong'),
('bob@example.com', 'Bob', 'Nguyen'),
('charlie@example.com', 'Charlie', 'Smith'),
('diana@example.com', 'Diana', 'Lee'),
('edward@example.com', 'Edward', 'Chen');

-- Agent
INSERT INTO agent VALUES
('alice@example.com', 'Senior Agent', 'Skyline Realty'),
('bob@example.com', 'Leasing Agent', 'Urban Nest'),
('charlie@example.com', 'Sales Associate', 'Cityscape Realty'),
('diana@example.com', 'Field Agent', 'Metro Realty'),
('edward@example.com', 'Junior Agent', 'Oceanic Estates');

-- Prospective Renter
INSERT INTO prospective_renter VALUES
('frank@example.com', '2025-06-01', 2500.00),
('grace@example.com', '2025-07-15', 1800.00),
('hannah@example.com', '2025-08-01', 2200.00),
('ian@example.com', '2025-05-20', 1900.00),
('jane@example.com', '2025-09-10', 2400.00);

-- Property
INSERT INTO property VALUES
('P1001', 'Chicago', 'IL', 'Modern 2BR condo downtown.', 2300.00, 1200, 'alice@example.com', 'Downtown'),
('P1002', 'Chicago', 'IL', 'Cozy 1BR near the park.', 1700.00, 800, 'bob@example.com', 'Uptown'),
('P1003', 'Chicago', 'IL', 'Spacious 3BR family house.', 2600.00, 1800, 'charlie@example.com', 'Midtown'),
('P1004', 'Chicago', 'IL', 'Luxury loft with skyline views.', 3200.00, 1500, 'diana@example.com', 'Downtown'),
('P1005', 'Chicago', 'IL', 'Commercial unit with high foot traffic.', 4000.00, 2200, 'edward@example.com', 'Harborview');

-- House
INSERT INTO house VALUES
('P1002', 1, 1),
('P1003', 3, 2),
('P1005', 0, 1),
('P1001', 2, 2),
('P1004', 2, 2);

-- Apartments
INSERT INTO apartments VALUES
('P1001', 2, 2, 'High-rise'),
('P1002', 1, 1, 'Low-rise'),
('P1003', 3, 2, 'Garden-style'),
('P1004', 2, 2, 'Penthouse'),
('P1005', 0, 1, 'Mixed-use');

-- Com Bldgs
INSERT INTO com_bldgs VALUES
('P1005', 'Retail'),
('P1002', 'Office'),
('P1003', 'Restaurant'),
('P1001', 'Cafe'),
('P1004', 'Boutique');

-- Land
INSERT INTO land VALUES
('P1005', 'Clay', 'Flat', 'Commercial'),
('P1002', 'Sandy', 'Hilly', 'Residential'),
('P1003', 'Loam', 'Flat', 'Industrial'),
('P1001', 'Rocky', 'Flat', 'Agricultural'),
('P1004', 'Peaty', 'Hilly', 'Mixed-use');

-- Vacation Home
INSERT INTO vacation_home VALUES
('P1001', 2, 2),
('P1002', 1, 1),
('P1003', 3, 2),
('P1004', 2, 2),
('P1005', 4, 3);

-- Booking
INSERT INTO booking VALUES
('B001', '2025-04-20', 300, '1234567890123456', '2025-07-01', '2025-08-01', 'frank@example.com', 'P1001'),
('B002', '2025-04-21', 250, '9876543210987654', '2025-08-10', '2025-09-10', 'grace@example.com', 'P1002'),
('B003', '2025-04-22', 180, '1111222233334444', '2025-06-15', '2025-07-15', 'hannah@example.com', 'P1003'),
('B004', '2025-04-23', 200, '5555666677778888', '2025-07-20', '2025-08-20', 'ian@example.com', 'P1004'),
('B005', '2025-04-24', 350, '9999000011112222', '2025-05-01', '2025-06-01', 'jane@example.com', 'P1005');

-- Address
INSERT INTO address VALUES
('frank@example.com', '123', 'Maple St', 'Chicago', 'IL', '60601'),
('grace@example.com', '456', 'Oak Ave', 'Chicago', 'IL', '60602'),
('hannah@example.com', '789', 'Pine Rd', 'Chicago', 'IL', '60603'),
('ian@example.com', '321', 'Elm St', 'Chicago', 'IL', '60604'),
('jane@example.com', '654', 'Birch Blvd', 'Chicago', 'IL', '60605');

-- Credit Card
INSERT INTO credit_card VALUES
('frank@example.com', '1234567890123456', '2027-12-01', '321'),
('grace@example.com', '9876543210987654', '2026-06-01', '654'),
('hannah@example.com', '1111222233334444', '2028-03-01', '987'),
('ian@example.com', '5555666677778888', '2025-11-01', '111'),
('jane@example.com', '9999000011112222', '2029-08-01', '222');

-- Preferred Location
INSERT INTO preferred_loc VALUES
('frank@example.com', 'Chicago', 'IL', 1),
('grace@example.com', 'Chicago', 'IL', 2),
('hannah@example.com', 'Evanston', 'IL', 1),
('ian@example.com', 'Chicago', 'IL', 3),
('jane@example.com', 'Naperville', 'IL', 1);

-- Amenities
INSERT INTO amenities VALUES
('P1001', TRUE, TRUE, TRUE, TRUE),
('P1002', TRUE, TRUE, FALSE, TRUE),
('P1003', TRUE, FALSE, TRUE, FALSE),
('P1004', TRUE, TRUE, TRUE, TRUE),
('P1005', FALSE, TRUE, TRUE, FALSE);

-- Reward Program
INSERT INTO reward_program VALUES
('RWD001', 300, 'frank@example.com'),
('RWD002', 250, 'grace@example.com'),
('RWD003', 180, 'hannah@example.com'),
('RWD004', 200, 'ian@example.com'),
('RWD005', 350, 'jane@example.com');

-- Looks At
INSERT INTO looks_at VALUES
('alice@example.com', 'B001'),
('bob@example.com', 'B002'),
('charlie@example.com', 'B003'),
('diana@example.com', 'B004'),
('edward@example.com', 'B005');

-- Makes
INSERT INTO makes VALUES
('frank@example.com', 'B001'),
('grace@example.com', 'B002'),
('hannah@example.com', 'B003'),
('ian@example.com', 'B004'),
('jane@example.com', 'B005');
