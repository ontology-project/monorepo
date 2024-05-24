import { Box, Button, Heading, Select, SimpleGrid, Text } from "@chakra-ui/react";
import AuthCheck from "../../components/AuthCheck";
import { QUERIES } from "../../utils/constants";
import { apiGet } from "../../utils/api";
import { useEffect, useState } from "react";


interface QueryPageProps {
}

const QueryPage: React.FC<QueryPageProps> = () => {
    const [curriculumOptions, setCurriculumOptions] = useState<string[]>();
    const [curriculum, setCurriculum] = useState<string>();

    useEffect(() => {
        const fetchClasses = async () => {
          try {
            const data = await apiGet('api/graphdb/get-curriculums');
            setCurriculumOptions(data.curriculums);  
          } catch (error: any) {
            console.log("error fetching curriculums", error)
          }
        };
      
        fetchClasses();
      }, []);

    const handleButtonClick = async (endpoint: string) => {
        try {
          const data = await apiGet(endpoint, { curriculum: curriculum });
          console.log("data:", data);
        } catch (error: any) {
          console.error("error!!!", error);
        }
      };

    if (!curriculumOptions) {
        return null;
    }

    return (
        <AuthCheck>
            <Box padding={10}>
                <Heading mb={4}>Query Page</Heading>
                <Text>Select Curriculum</Text>
                <Select mb={4} value={curriculum} onChange={(e) => setCurriculum(e.target.value)}>
                    {curriculumOptions.map((curr) => (
                        <option key={curr} value={curr}>
                            {curr}
                        </option>
                    ))}
                </Select>
                <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
                    {QUERIES.map((query, index) => (
                        <Button key={index} size="lg" padding={8} onClick={() => handleButtonClick(query.endpoint)}>
                            <Text noOfLines={3} wordBreak="break-word" whiteSpace="normal">
                                {query.text}
                            </Text>
                        </Button>
                    ))}
                </SimpleGrid>
            </Box>
        </AuthCheck>
    )
}

export default QueryPage;