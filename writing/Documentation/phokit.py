class phokit(object):
    """
    Instantiates an instance of phokit. The phokit object itself holds the list of tagged words, 
    the segmental inventories, and non-default specifications after the stim list and spec files 
    have been uploaded with the loadFiles() method. The consonant and vowel durations default to 
    100 and can be modified with the setDefault() method.
    
    Attributes:
    wordlist (list): Stores each line of the stim list as an item.
    specs (dict): Holds the spec file key-value pairs.
    durC (int): The default consonant length in milliseconds. The default is 100.
    durV (int): The default vowel length in milliseconds. The default is 100.
    listC (list): A list of the consonants in the spec file.
    listV (list): A list of the vowels in the spec file.
    counter (int): Used to assign a unique numerical value in file names.
    
    """
    def __init__(self):

        self.wordlist=[]
        self.specs={}
        self.durC= 100
        self.durV= 100
        self.listC = []
        self.listV = []
        self.counter=0
        
    def loadFiles(self, wordFile, specificationFile):
        """
        Loads the stim list and spec file into a phokit instance.
        
        Arg:
        wordFile (file): the stim list, a .txt file 
        specificationFile (file): the spec file, a .txt file
        
        """
        # Opens the word list file and reads in the lines. Each line of text becomes one item in a list called wordFile_lines.
        wordFile_raw = open(wordFile, 'r')
        wordFile_lines = wordFile_raw.readlines()
        wordFile_raw.close()
        
        # Removes the '\n' (i.e. the newline character) from the end of each element in wordFile_lines then appends that to
        # self.wordlist which is a list of words stored in a phokit instance.
        for word in wordFile_lines:
            self.wordlist.append(word.strip())
        
        # Opens the specifications file and converts each line (which should be of the format 'text1: text2') and 
        # converts that line into a dictionary key:value pair to be stored in the phonkit instance variable self.specs
        with open(specificationFile) as f:
            for line in f:
                (key, val) = line.split(':')
                self.specs[key] = val.strip()
        
        # Sets the default consonant and vowel durations to the values specified for 'cduration' and 'vduration' respectively.
        self.durC=self.specs['cduration']=int(self.specs['cduration'])
        self.durV=self.specs['vduration']=int(self.specs['vduration'])
        
        # Sets the phokit object's self.listC and self.listV to the consonant and vowel lists provided by the user in the specification file.
        self.listC=self.specs['consonants'].split()
        self.listV=self.specs['vowels'].split()
        
    def setDefault(cduration, vduration):
        """
        Changes the default consonant and vowel durations from 100 to the desired values.
        
        Arg:
        cduration (int): the new consonant duration in milliseconds 
        vduration (int): the new vowel duration in milliseconds
        
        Ex: 
        >>> print tomsvoice.durC, tomsvoice.durV
        100, 100
        >>> tomsvoice.setDefault(75, 80)
        >>> print tomsvoice.durC, tomsvoice.durV
        75, 80
        
        """
        self.durC = cduration
        self.durV = vduration
        
    def make(self, tagged_word):
        """
        Makes a .pho file based on the string provided.
        
        Arg:
        tagged_word (str): the contents of the desired .pho file
        
        Ex:
        >>> tomsvoice.make(’p a<dur:200> t a’)
        >>>
        
        """
        # Import the re module
        import re
        
        # Split the tagged_word on spaces and yields a list of the remaining elements
        seg_list = tagged_word.split()
        
        # Create a place holder for the stimulus name
        stimname=[]
        # Defines the list of illegal filename characters
        illegal_chars="/?<>\:*|"
        # A regular expression for finding duration tags. The duration value is saved as a group named 'duration'.
        reDur= re.compile(r'<dur:(?P<duration>\d*)>')
        # Updates the counter, which is used to ensure unique names for tokens.
        self.counter+=1
        
        # For each segment in seg_list
        for seg in seg_list:
            # If the segment is untagged, extend stimname to include the segment.
            if (seg in self.listC) or (seg in self.listV):
                stimname.extend(seg)
            # If the segment is tagged, extract the segment and extend stimname by it.
            else:
                seg_tagged = reDur.sub(r' \g<duration>', seg)
                seg_split_from_tag= seg_tagged.partition(' ')
                stimname.extend(seg_split_from_tag[0])
        
        # Join the list of segments in stimname into a string
        stimname= ''.join(stimname)
        
        # If the stimname string contains characters that would be illicit for filenames, remove the offending character.
        for seg in stimname:
            if seg in illegal_chars:
                stimname=stimname.replace(seg, "")
        
        # Concatinate the stimname, current counter number, and .pho file extension and assign it to the variable filename.
        filename = stimname+str(self.counter)+'.pho'
        
        # Create a new file whose name is filename.
        theFile = open(filename, "wb")
       
        # If the segment in seg_list is...
        for seg in seg_list:
            # a consonant, write a newline to the file that contains the consonant followed by a space and then the default duration for consonants.
            if seg in self.listC:
                theFile.write(seg+' '+str(self.durC)+'\n')
            # a vowel, write a newline to the file that contains the vowel followed by a space and then the default duration for vowels.
            elif seg in self.listV:
                 theFile.write(seg+' '+str(self.durV)+'\n')
            # a tagged segment, write a newline to the file that contains the vowel followed by a space and then the specified duration value.
            else:
                segTagged = reDur.sub(r' \g<duration>', seg)
                theFile.write(segTagged+'\n')
        
        # Close the file.
        theFile.close()
        
    
    def makeAll(self):
        """
        Creates a .pho file for each line in the stim list that was loaded into the phokit object.
        """
        for word in self.wordlist:
            self.make(word)
        
    def inspect(self, tagged_word):
        """
        Returns an easy-to-read version of a stim list line. The first line containts the segments of 
        the input. The second line displays the durations each segment under that segment. Default
        values are not displayed.
        
        Arg:
        tagged_word (str): the .pho file content to inspect
        
        Ex:
        >>> phokit.inspect('p a<dur:150> t a')
        >>> word:    p    a    t    a
        >>> dur:          150
        
        """ 
        
        # Import the re module.
        import re
        
        # Split the tagged_word on spaces and yields a list of the remaining elements.
        seg_list = tagged_word.split()
        
        # Create a place holder for the stimulus name and duration values.
        stimname=[]
        stimdur=[]
        for_default_values='-'

        # A regular expression for finding duration tags. The duration value is saved as a group named 'duration'.
        reDur= re.compile(r'<dur:(?P<duration>\d*)>')
        
        # For each segment in seg_list
        for seg in seg_list:
            # If the segment is untagged, extend stimname to include the segment.
            if seg in self.listC:
                stimname.extend(seg)
                stimdur.append(for_default_values)
            elif seg in self.listV:
                stimname.extend(seg)
                stimdur.append(for_default_values)
            # If the segment is tagged, extract the segment and extend stimname by it. Append to stimdur the duration
            # specified in the segment's duration tag.
            else:
                seg_tagged = reDur.sub(r' \g<duration>', seg)
                seg_split_from_tag= seg_tagged.partition(' ')
                stimname.extend(seg_split_from_tag[0])
                stimdur.append(str(seg_split_from_tag[2]))
                
        # Prints a 'table' for inspecting word values.
        print '{word:10}\t'.format(word='word:'), 
        
        for phone in stimname:
            print '{seg:^5}\t'.format(seg=phone),
        
        print
        
        print '{dur:10}\t'.format(dur='dur:'), 
            
        for value in stimdur:
            print '{dur:^5}\t'.format(dur=value),
        
        print  '\n','\n'