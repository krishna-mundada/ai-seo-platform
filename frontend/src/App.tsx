import { AppShell, Burger, Group, Text, NavLink, ScrollArea } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { Routes, Route, useLocation, Link } from 'react-router-dom'
import { 
  IconDashboard, 
  IconFileText, 
  IconBuildingStore, 
  IconSpeakerphone, 
  IconSettings,
  IconSparkles
} from '@tabler/icons-react'
import { Dashboard } from './pages/Dashboard'
import { ContentGenerator } from './pages/ContentGenerator'
import { ContentList } from './pages/ContentList'
import { BusinessManagement } from './pages/BusinessManagement'

const navigationItems = [
  { icon: IconDashboard, label: 'Dashboard', link: '/' },
  { icon: IconSparkles, label: 'Generate Content', link: '/generate' },
  { icon: IconFileText, label: 'Content', link: '/content' },
  { icon: IconBuildingStore, label: 'Businesses', link: '/businesses' },
  { icon: IconSpeakerphone, label: 'Campaigns', link: '/campaigns' },
  { icon: IconSettings, label: 'Settings', link: '/settings' },
]

export default function App() {
  const [opened, { toggle }] = useDisclosure()
  const location = useLocation()

  return (
    <AppShell
      header={{ height: 60 }}
      navbar={{
        width: 280,
        breakpoint: 'sm',
        collapsed: { mobile: !opened },
      }}
      padding="md"
    >
      <AppShell.Header>
        <Group h="100%" px="md">
          <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
          <Group>
            <IconSparkles size={28} style={{ color: 'var(--mantine-color-blue-6)' }} />
            <Text size="xl" fw={700} c="blue">
              AI SEO Platform
            </Text>
          </Group>
        </Group>
      </AppShell.Header>

      <AppShell.Navbar p="md">
        <AppShell.Section grow my="md" component={ScrollArea}>
          {navigationItems.map((item) => (
            <NavLink
              key={item.label}
              component={Link}
              to={item.link}
              label={item.label}
              leftSection={<item.icon size={20} />}
              active={location.pathname === item.link}
              variant="subtle"
              mb="xs"
            />
          ))}
        </AppShell.Section>
      </AppShell.Navbar>

      <AppShell.Main>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/generate" element={<ContentGenerator />} />
          <Route path="/content" element={<ContentList />} />
          <Route path="/businesses" element={<BusinessManagement />} />
          <Route path="/campaigns" element={<div>Campaigns (Coming Soon)</div>} />
          <Route path="/settings" element={<div>Settings (Coming Soon)</div>} />
        </Routes>
      </AppShell.Main>
    </AppShell>
  )
}
