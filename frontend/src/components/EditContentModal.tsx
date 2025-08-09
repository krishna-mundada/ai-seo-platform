import { Stack, Group, Text, Button, TextInput, Textarea, Card } from '@mantine/core'
import { useState, useEffect } from 'react'
import { IconCheck } from '@tabler/icons-react'

interface EditContentModalProps {
  opened: boolean
  onClose: () => void
  title: string
  content: string
  onSave: (title: string, content: string) => void
}

export function EditContentModal({ opened, onClose, title, content, onSave }: EditContentModalProps) {
  const [editedTitle, setEditedTitle] = useState(title)
  const [editedContent, setEditedContent] = useState(content)

  useEffect(() => {
    setEditedTitle(title)
    setEditedContent(content)
  }, [title, content])

  const handleSave = () => {
    onSave(editedTitle, editedContent)
    onClose()
  }

  if (!opened) return null

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '20px'
    }}>
      <Card 
        style={{ 
          width: '90%', 
          maxWidth: '800px', 
          maxHeight: '80vh', 
          overflow: 'auto' 
        }}
        shadow="xl"
        padding="xl"
      >
        <Stack gap="md">
          <Group justify="space-between">
            <Text size="lg" fw={700}>Edit Content</Text>
            <Button variant="subtle" size="sm" onClick={onClose}>✕</Button>
          </Group>
          
          <TextInput
            label="Title"
            placeholder="Enter content title"
            value={editedTitle}
            onChange={(event) => setEditedTitle(event.currentTarget.value)}
            required
          />
          
          <Textarea
            label="Content"
            placeholder="Enter your content here..."
            value={editedContent}
            onChange={(event) => setEditedContent(event.currentTarget.value)}
            minRows={12}
            maxRows={20}
            autosize
            required
          />
          
          <Group justify="flex-end" gap="sm">
            <Button variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button 
              onClick={handleSave}
              leftSection={<IconCheck size={16} />}
            >
              Save Changes
            </Button>
          </Group>
        </Stack>
      </Card>
    </div>
  )
}