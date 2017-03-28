package org.lappsgrid.example;
import org.lappsgrid.api.ProcessingService;
import org.lappsgrid.discriminator.Discriminators.Uri;
// additional API for metadata
import org.lappsgrid.metadata.IOSpecification;
import org.lappsgrid.metadata.ServiceMetadata;
import org.lappsgrid.serialization.Data;
import org.lappsgrid.serialization.DataContainer;
import org.lappsgrid.serialization.Serializer;
import org.lappsgrid.serialization.lif.Annotation;
import org.lappsgrid.serialization.lif.Container;
import org.lappsgrid.serialization.lif.View;
import org.lappsgrid.vocabulary.Features;

import java.util.List;

import org.json.*;



/**
 * Requires: JSON in LIF/LAPPS produced from NGram service 
 * <p> 
 * Effects: This class will use the view produced by NGram and produce 
 * a score for each answer using BOW model
 * <p>
 * The annotations contain the score for each sentence, and inherited features
 *           
 */
public class input implements ProcessingService
{
    /**
     * The Json String required by getMetadata()
     */
    private String metadata;


    public input() {

        metadata = generateMetadata();

    }

    private String generateMetadata() {
        // Create and populate the metadata object
        ServiceMetadata metadata = new ServiceMetadata();

        // Populate metadata using setX() methods
        metadata.setName(this.getClass().getName());
        metadata.setDescription("input");
        metadata.setVersion("1.0.0-SNAPSHOT");
        metadata.setVendor("http://www.lappsgrid.org");
        metadata.setLicense(Uri.APACHE2);

        // JSON for input information
        IOSpecification requires = new IOSpecification();
        requires.addFormat(Uri.LIF);            // LIF (form)
        requires.addLanguage("en");             // Source language
        requires.setEncoding("UTF-8");

        // JSON for output information
        IOSpecification produces = new IOSpecification();
        produces.addFormat(Uri.LAPPS);          // LIF (form) synonymous to LIF
        produces.addAnnotation(Uri.SENTENCE);      // Tokens (contents)
        requires.addLanguage("en");             // Target language
        produces.setEncoding("UTF-8");

        // Embed I/O metadata JSON objects
        metadata.setRequires(requires);
        metadata.setProduces(produces);

        // Serialize the metadata to a string and return
        Data<ServiceMetadata> data = new Data<ServiceMetadata>(Uri.META, metadata);
        return data.asPrettyJson();
    }
    
    
    @Override
    /**
     * getMetadata simply returns metadata populated in the constructor
     */
    public String getMetadata() {
        return metadata;
    }

    @Override
    public String execute(String input) {
        // Step #1: Parse the input.
        Data data = Serializer.parse(input, Data.class);

        // Step #2: Check the discriminator
        final String discriminator = data.getDiscriminator();
        if (discriminator.equals(Uri.ERROR)) {
            // Return the input unchanged.
            return input;
        }

        // Step #3: Extract the text.
        Container container = null;
        if (discriminator.equals(Uri.JSON)) {
          container = new Container();
//          container.setText(data.getPayload().toString());
      }
        else {
            // This is a format we don't accept.
            String message = String.format("Unsupported discriminator type: %s", discriminator);
            return new Data<String>(Uri.ERROR, message).asJson();
        }

        // Step #4: Create a new View
        View view = container.newView();
        String text = data.getPayload().toString();
//        String text = container.getText();
        //Replace the Quotation mark to work
        //Can be improved
        text = text.replaceAll("\"", "");
        JSONObject obj = null;
//        System.out.println(text);
        try {
          obj = new JSONObject(text);
        } catch (JSONException e) {
          // TODO Auto-generated catch block
          e.printStackTrace();
        }

        try {
          String question = obj.getString("question");
          String[] temp =question.substring(1, question.length() - 1).replaceAll("\"","").split(",");
          question = String.join(",", temp);
          String passage = obj.getString("passage");
          temp =passage.substring(1, passage.length() - 1).replaceAll("\"","").split(",");
          passage = String.join(",", temp);
          String answer = obj.getString("true_answers.text");
          temp =answer.substring(1, answer.length() - 1).replaceAll("\"","").split(",");
          answer = String.join(",", temp);
          String id = obj.getString("id");
          
          Annotation a = view.newAnnotation("Q", Uri.SENTENCE, 0, 0);
          a.addFeature(Features.Sentence.TARGETS, question);
          a.addFeature(Features.Sentence.TYPE, "Question");
          
          int start = obj.getJSONArray("true_answers.begin").getInt(0);
          int end = obj.getJSONArray("true_answers.end").getInt(0);
          a = view.newAnnotation("A", Uri.SENTENCE, start, end);
          a.addFeature(Features.Sentence.TARGETS, answer);
          a.addFeature(Features.Sentence.TYPE, "Answer");
          
          a = view.newAnnotation("P", Uri.SENTENCE, 0, passage.length());
          a.addFeature(Features.Sentence.TARGETS, passage);
          a.addFeature(Features.Sentence.TYPE, "Passage");
        } catch (JSONException e) {
          // TODO Auto-generated catch block
          e.printStackTrace();
        }
          // TODO Auto-generated catch block
          
        
//        System.out.println(temp.get("question"));
        // Step #7: Create a DataContainer with the result.
        data = new DataContainer(container);

        // Step #8: Serialize the data object and return the JSON.
        return data.asPrettyJson();
    }
}
