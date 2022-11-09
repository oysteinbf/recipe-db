INSERT INTO recipe (name, introduction, prep_time, cook_time, source, tags, n_servings)
VALUES 
   ('Tomatsuppe', 'En klassisk favoritt!', 20, 30, 'Mias mat', 'vegetar, høst', 4),
   ('Poke bowl', 'En laksesalat proppfull av masse deilig smak, inspirert fra Hawaii', 30, 0, ' Silje Feiring / Spoon.no', NULL, 4),
   ('Butter chicken', 'En indisk vinner', 60, 40, NULL, 'kylling, indisk', 4),
   ('Taco', NULL, NULL, NULL, NULL, NULL, 2);

INSERT INTO ingredient (name, description, category)
VALUES 
   ('Tomat(er)', 'Rød grønnsak', 'Grønnsak'),
   ('Kylling', NULL, 'Kjøtt'),
   ('Sitronsaft', NULL, NULL),
   ('Koriander', NULL, NULL),
   ('Mango', NULL, NULL),
   ('Hvitløk', NULL, NULL),
   ('Løk', NULL, NULL),
   ('Vårløk', NULL, 'Grønnsak'),
   ('Garam masala', NULL, 'Krydder'),
   ('Ris', NULL, NULL),
   ('Laks', NULL, 'Fisk'),
   ('Hakkede tomater', NULL, 'Hermetikk'),
   ('Soyasaus', NULL, NULL),
   ('Sesamolje', NULL, NULL),
   ('Sesamfrø', NULL, NULL),
   ('Riseddik', NULL, NULL),
   ('Sukker', NULL, NULL),
   ('Avokado', NULL, NULL),
   ('Sjalottløk', NULL, NULL),
   ('Chili', NULL, NULL),
   ('Tomatpuré', NULL, NULL),
   ('Grønnsakskraft', NULL, NULL);

INSERT INTO method (recipe_id, step_number, step_description)
VALUES
   (1, 1, 'Ha olivenolje eller en annen nøytral matolje i en gryte og fres løken på middels varme, til den er blank og myk, men uten at den tar farge. Mot slutten tilsetter du hvitløk og chili, og lar det surre med. Mengden chili og hvitløk regulerer du etter smak og behag.'),
   (1, 2, 'Tilsett tomatpureèn og la det surre med et par minutter.'),
   (1, 3, 'Tilsett de hermetiske tomatene, knus dem lett med en stekespade eller lignende, og gi suppen et oppkok. Tilsett deretter kraften og kok opp igjen. Har du ikke kraft tilgjengelig kan du fint benytte buljongterninger eller fond utblandet i vann. Det er her viktig å smake seg frem til du får ønsket smak på suppen din. Tomatsmaken skal være dominerende, og kraften skal gi ytterligere smak. Tilsett eventuelt litt sukker dersom du ønsker litt mer sødme på suppen din.'),
   (1, 4, 'La suppen småkoke til tomatene er møre og fine. Det tar ca 15-20 minutter dersom du benytter hele tomater. Benytter du hakkede tomater kan koketiden gjerne reduseres til ca 10. minutter hvis du har det travelt eller er veldig sulten. Kjør suppen med en stavmikser eller lignende, til du får en jevn suppe. Tilsett eventuelt mer vann eller kraft hvis du synes suppen blir for tykk. Smak til med nykvernet sort pepper og salt.'),
   (2, 1, 'Kok ris etter anvisning på pakken. Avkjøl. '),
   (2, 2, 'Bland sammen soyasaus, sesamolje, riseddik og sukker til en marinade. Del laks i terninger og vend i marinaden. La stå noen minutter.'),
   (2, 3, 'Rens og kutt vårløk, avocado og mango i tynne strimler.'), 
   (2, 4, 'Fordel ris, marinert laks, mango, avocado og vårløk i serveringskåler.'),
   (2, 5, 'Server poke bowl med laks. Topp med grovhakket koriander og sesamfrø.'),
   (3, 1, 'Steg 1 blabla'),
   (3, 2, 'Steg 2 blabla'),
   (3, 3, 'Steg 3 blabla'),
   (3, 4, 'Steg 4 blabla'),
   (4, 1, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec leo quam, porta sed orci at, fringilla tristique est. Fusce iaculis, magna id lobortis imperdiet, nisl odio pharetra dui, ut dapibus libero urna id ante. Curabitur velit eros, venenatis accumsan euismod id, finibus a dui. Suspendisse potenti.'),
   (4, 2, 'Quisque tincidunt ornare sem, et mollis tortor egestas non. Nulla suscipit augue ac pulvinar dapibus. Quisque maximus cursus ex vitae ultrices. '),
   (4, 3, 'Nulla efficitur vulputate posuere. Suspendisse nisl justo, convallis sed ipsum in, ullamcorper luctus arcu. Vestibulum imperdiet augue non dolor suscipit, eu ullamcorper risus laoreet. Fusce lobortis viverra vestibulum. Aliquam nisi justo, faucibus ac dictum a, eleifend quis ex. Ut convallis erat lacus, non dignissim lacus cursus quis. Integer sed efficitur neque. Morbi et ultricies massa. Proin sit amet felis velit. '),
   (4, 4, 'Aliquam et neque sit amet velit eleifend suscipit.'),
   (4, 5, 'Suspendisse vestibulum enim vitae sagittis cursus. Etiam at felis malesuada, maximus ex at, tristique mi. Nunc venenatis velit purus, nec convallis magna rhoncus non. Proin luctus, tellus ac vulputate aliquam, lectus quam vestibulum lacus, in consequat augue purus malesuada nisi. Ut lacinia arcu leo, ac scelerisque tortor feugiat eu. Donec leo dolor, sagittis a finibus at, malesuada ut mi. Sed vel tortor bibendum, ultrices lacus vel, semper massa. Vivamus cursus, erat vel ornare consequat, lectus lectus tempus diam, quis dapibus tortor ante eget libero. Aenean pulvinar odio aliquet tellus imperdiet tempus. Suspendisse cursus velit eu sapien ultricies rutrum. Fusce diam massa, blandit eu dui nec, consectetur rutrum ante. Phasellus egestas facilisis ullamcorper. Quisque ac volutpat est, sed dictum nunc. Proin venenatis turpis id ligula egestas elementum. Mauris nec mi nec erat facilisis aliquam.');


INSERT INTO bridge_recipe_ingredient (recipe_id, ingredient_id, amount, unit, preparation_info, multiplication_factor)
VALUES
   (1, 6, 3, 'fedd', 'finhakket', 2),
   (1, 19, 2, 'stk', 'finhakket', 2),
   (1, 20, 0.5, 'stk', 'finhakket', 2),
   (1, 21, 2, 'ss', NULL, 2),
   (1, 12, 2, 'bokser', NULL, 2),
   (1, 22, 7.5, 'dl', NULL, 2),
   (2, 13, 4, 'ss', NULL, 2),
   (2, 14, 2, 'ss', NULL, 2),
   (2, 16, 3, 'ss', NULL, 2),
   (2, 17, 1, 'ss', NULL, 2),
   (2, 18, 2, 'stk', NULL, 2),
   (2, 11, 600, 'g', NULL, 2),
   (2, 8, 3, 'stk', NULL, 2),
   (2, 4, 20, 'g', NULL, 2),
   (2, 15, 2, 'ss', NULL, 2),
   (3, 2, 400, 'g', NULL, 2);

INSERT INTO category (name, symbol, color_code)
VALUES
   ('Suppe', 'some_link', '(255, 165, 0)'),
   ('Fisk', 'some_link', '(0, 0, 255)'),
   ('Vegetar', 'some_link', NULL),
   ('Indisk', 'some_link', NULL);

INSERT INTO bridge_recipe_category (recipe_id, category_id)
VALUES
  (1, 1),
  (1, 3),
  (2, 2),
  (3, 4);
