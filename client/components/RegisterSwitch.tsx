import { Box, Tabs, TabList, Tab } from "@chakra-ui/react";
import { useState } from "react";

const RegisterSwitch: React.FC = () => {
  const [role, setRole] = useState<'kaprodi' | 'reviewer'>('kaprodi');

  const handleRoleChange = (index: number) => {
    if (index === 0) {
      setRole('kaprodi');
    } else {
      setRole('reviewer');
    }
  };

  return (
    <Box>
      <Tabs index={role === 'kaprodi' ? 0 : 1} onChange={handleRoleChange} variant="soft-rounded">
        <TabList>
          <Tab flex="1" textAlign="center">Kaprodi</Tab>
          <Tab flex="1" textAlign="center">Reviewer</Tab>
        </TabList>
      </Tabs>
    </Box>
  );
};

export default RegisterSwitch;
