import ChatInterface from './ChatInterface';

function App() {
  const currentUserId = 5; // Get from your auth system
  const otherUserId = 10;   // Selected chat
  const otherUserName = "Sara";

  return (
    <ChatInterface
      currentUserId={currentUserId}
      otherUserId={otherUserId}
      otherUserName={otherUserName}
    />
  );
}