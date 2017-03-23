package org.lappsgrid.example;
import org.lappsgrid.api.ProcessingService;
import org.lappsgrid.discriminator.Discriminators.Uri;

import org.lappsgrid.serialization.Data;
import org.lappsgrid.serialization.DataContainer;
import org.lappsgrid.serialization.LappsIOException;
import org.lappsgrid.serialization.Serializer;
import org.lappsgrid.serialization.lif.Annotation;
import org.lappsgrid.serialization.lif.Container;
import org.lappsgrid.serialization.lif.View;
import org.lappsgrid.vocabulary.Features;

// additional API for metadata
import org.lappsgrid.metadata.IOSpecification;
import org.lappsgrid.metadata.ServiceMetadata;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.Set;


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
        metadata.setDescription("AnswerScoring");
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
        produces.addAnnotation(Uri.TOKEN);      // Tokens (contents)
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
        if (discriminator.equals(Uri.LAPPS)) {
            container = new Container((Map) data.getPayload());
        }
        else {
            // This is a format we don't accept.
            String message = String.format("Unsupported discriminator type: %s", discriminator);
            return new Data<String>(Uri.ERROR, message).asJson();
        }

        // Step #4: Create a new View
        List<View> views = container.getViews();
        int len = views.size();
        View pre_view = container.getView(len - 1);
        List<Annotation> annotations = pre_view.getAnnotations();
        
        container = new Container();
        
        View view = container.newView();
        int id = -1;
       Annotation question = annotations.get(0);
        
       Annotation s = view.newAnnotation("S" + (++id), Uri.TOKEN, question.getStart(), question.getEnd());
       s.addFeature(Features.Token.TYPE, question.getFeature(Features.Token.TYPE));
       s.addFeature(Features.Token.ID, question.getFeature(Features.Token.ID));
       int a_len = annotations.size();
       for(int i = 1; i < a_len; i ++){
         Annotation anwser = annotations.get(i);
         long start = anwser.getStart();
         long end = anwser.getEnd();
         s = view.newAnnotation("S" + (++id), Uri.TOKEN, (int)start, (int)end);
         for(int j = 1; j <= 3; j ++){
           String name = j + "-Gram";
           Map<String, Integer> q = null;
           try {
             q = new HashMap<String, Integer>(
                     question.getFeatureMap(name));
           } catch (LappsIOException e) {
             e.printStackTrace();
           }
           Map<String, Integer> a = null;
           try {
             a = new HashMap<String, Integer>(anwser.getFeatureMap(name));
           }
           catch (LappsIOException e) {
             e.printStackTrace();
           }
           double score = 0;
           for(String key: q.keySet()){
             if(a.containsKey(key)){
//                 score += a.get(key);
               score += 1;
             }
           }
           score = score / q.size();
           s.addFeature(name, String.format("%.2f", score));
         }
   
           s.addFeature(Features.Token.TYPE, anwser.getFeature(Features.Token.TYPE));
           s.addFeature(Features.Token.ID, anwser.getFeature(Features.Token.ID));
           s.addFeature("isCorrect", anwser.getFeature("isCorrect"));
       }
       
        // Step #6: Update the view's metadata. Each view contains metadata about the
        // annotations it contains, in particular the name of the tool that produced the
        // annotations.
        view.addContains(Uri.TOKEN, this.getClass().getName(), "AnswerScoring");

        // Step #7: Create a DataContainer with the result.
        data = new DataContainer(container);

        // Step #8: Serialize the data object and return the JSON.
        return data.asPrettyJson();
    }
}
